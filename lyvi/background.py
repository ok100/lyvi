# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os
from io import BytesIO
#from threading import Timer

from PIL import Image

import lyvi
from lyvi.utils import check_output


if 'TMUX' in os.environ:
    BG_BEG = 'printf "\ePtmux;\e\e]20;'   
    BG_END = ';100x100+50+50:op=keep-aspect\a\e\\\\"'
else:
    BG_BEG = 'printf "\e]20;'
    BG_END = ';100x100+50+50:op=keep-aspect\a"'
BG_COLOR = '#FFFFFF'
for line in check_output('xrdb -query').splitlines():
    if 'background' in line:
        BG_COLOR = line.split(':')[1].strip()


class Background:
    def __init__(self):
        self.type = lyvi.config['bg_type']
        self.opacity = lyvi.config['bg_opacity']
        self.file = '%s/lyvi-%s.jpg' % (lyvi.TEMP, lyvi.PID)

    def toggle_type(self):
        self.type = 'cover' if self.type == 'backdrops' else 'backdrops'
        self.update()

    def blend(self, image, opacity):
        if isinstance(image, bytes):
            buf = BytesIO(image)
            image = Image.open(buf)
        layer = Image.new(image.mode, image.size, BG_COLOR)
        return Image.blend(image, layer, 1 - opacity)

    def update(self, clean=False):
        if ((self.type == 'backdrops' and lyvi.md.backdrops and lyvi.md.artist)
                or (self.type == 'cover' and lyvi.md.cover and lyvi.md.album)
                and not clean):
            image = self.blend(getattr(lyvi.md, self.type), self.opacity)
        else:
            image = Image.new('RGB', (100, 100), BG_COLOR)
        image.save(self.file)
        os.system(BG_BEG + self.file + BG_END)

    def cleanup(self):
        self.update(clean=True)
        os.remove(self.file)


class TmuxBackground(Background):
    title = lyvi.config['bg_tmux_window_title']
    cover_pane = lyvi.config['bg_tmux_cover_pane']
    backdrops_pane = lyvi.config['bg_tmux_backdrops_pane']

    def get_layout(self):
        class Pane: pass
        display = check_output('tmux display -p \'#{window_layout}\'')
        for delim in '[]{}':
            display = display.replace(delim, ',')
        layout = [Pane()]
        layout[0].w, layout[0].h = (int(a) for a in display.split(',')[1].split('x'))
        display = display.split(',', 1)[1]
        chunks = display.split(',')
        for i in range(0, len(chunks) - 1):
            if 'x' in chunks[i] and 'x' not in chunks[i + 3]:
                layout.append(Pane())
                layout[-1].w, layout[-1].h = (int(a) for a in chunks[i].split('x'))
                layout[-1].x = int(chunks[i + 1])
                layout[-1].y = int(chunks[i + 2])
        lsp = check_output('tmux lsp').splitlines()
        for chunk in lsp:
            layout[lsp.index(chunk) + 1].active = 'active' in chunk
        return layout

    def get_size(self):
        for line in check_output('xwininfo -name ' + self.title).splitlines():
            if 'Width:' in line:
                width = int(line.split()[1])
            elif 'Height:' in line:
                height = int(line.split()[1])
        return width, height

    def paste(self, root, image, pane, cell_w, cell_h, blend):
        buf = BytesIO(image)
        image = Image.open(buf)
        image.thumbnail((pane.w * cell_w, pane.h * cell_h), Image.ANTIALIAS)
        if blend:
            image = self.blend(image, self.opacity)
        x1 = (pane.x - 1) * cell_w
        y1 = (pane.y - 1) * cell_h
        x2 = (pane.x + pane.w) * cell_w
        y2 = (pane.y + pane.h) * cell_h
        root.paste(image, (round(x1 + (x2 - x1) / 2 - image.size[0] / 2),
                           round(y1 + (y2 - y1) / 2 - image.size[1] / 2)))
        return root

    def update(self, clean=False):
        layout = self.get_layout()
        width, height = self.get_size()
        cell_w = width / layout[0].w
        cell_h = height / layout[0].h
        image = Image.new('RGB', (width, height), BG_COLOR)
        cover_data = [
            lyvi.md.cover, 
            layout[self.cover_pane + 1],
            lyvi.config['bg_tmux_cover_underlying']
        ]
        backdrops_data = [
            lyvi.md.backdrops, 
            layout[self.backdrops_pane + 1],
            lyvi.config['bg_tmux_backdrops_underlying']
        ]
        if not clean:
            if self.backdrops_pane == self.cover_pane:
                to_paste = [cover_data] if self.type == 'cover' else [backdrops_data]
            else:
                to_paste = [cover_data, backdrops_data]
            for i in to_paste:
                if i[0]:
                    image = self.paste(image, i[0], i[1], cell_w, cell_h, i[2])
        image.save(self.file)
        os.system(BG_BEG + self.file + BG_END)
