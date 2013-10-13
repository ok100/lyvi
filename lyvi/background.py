# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os
from io import BytesIO

from PIL import Image

import lyvi
from lyvi.utils import check_output


BG_COLOR = '#FFFFFF'
for line in check_output('xrdb -query').splitlines():
    if 'background' in line:
        BG_COLOR = line.split(':')[1].strip()


def pil_image(image):
    if isinstance(image, bytes):
        buf = BytesIO(image)
        return Image.open(buf)
    return image


def blend(image, opacity):
    image = pil_image(image)
    layer = Image.new(image.mode, image.size, BG_COLOR)
    return Image.blend(image, layer, 1 - opacity)


def paste(root, image_to_paste, x, y):
    root = pil_image(root)
    image_to_paste = pil_image(image_to_paste)
    root.paste(image_to_paste, (x, y))
    return root


def resize(image, x, y):
    image = pil_image(image)
    image.thumbnail((x, y), Image.ANTIALIAS)
    return image


class Background:
    ESCAPE_STR_BEG = 'printf "\e]20;'
    ESCAPE_STR_END = ';100x100+50+50:op=keep-aspect\a"'

    def __init__(self):
        self.type = lyvi.config['bg_type']
        self.opacity = lyvi.config['bg_opacity']
        self.file = '%s/lyvi-%s.jpg' % (lyvi.TEMP, lyvi.PID)

    def toggle_type(self):
        self.type = 'cover' if self.type == 'backdrops' else 'backdrops'
        self.update()

    def _make(self, clean=False):
        if (((self.type == 'backdrops' and lyvi.md.backdrops and lyvi.md.artist)
                or (self.type == 'cover' and lyvi.md.cover and lyvi.md.album))
                and not clean):
            image = blend(getattr(lyvi.md, self.type), self.opacity)
        else:
            image = Image.new('RGB', (100, 100), BG_COLOR)
        image.save(self.file)

    def _set(self):
        os.system(self.ESCAPE_STR_BEG + self.file + self.ESCAPE_STR_END)

    def update(self, clean=False):
        self._make(clean=clean)
        self._set()

    def cleanup(self):
        self.update(clean=True)
        os.remove(self.file)


class Tmux:
    def __init__(self):
        class Cell: pass
        self.cell = Cell()
        self.update()

    def _get_layout(self):
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

    def _get_size_px(self):
        info = check_output('xwininfo -name ' + lyvi.config['bg_tmux_window_title'])
        try:
            width = int(info.split('Width: ')[1].split('\n')[0])
            height = int(info.split('Height: ')[1].split('\n')[0])
        except IndexError:
            width = height = 0
        return width, height
    
    def update(self):
        self.layout = self._get_layout()
        self.width, self.height = self._get_size_px()
        self.cell.w = round(self.width / self.layout[0].w)
        self.cell.h = round(self.height / self.layout[0].h)


class TmuxBackground(Background):
    ESCAPE_STR_BEG = 'printf "\ePtmux;\e\e]20;'   
    ESCAPE_STR_END = ';100x100+50+50:op=keep-aspect\a\e\\\\"'

    def __init__(self):
        super().__init__()
        self.tmux = Tmux()

    def _make(self, clean=False):
        self.tmux.update()
        image = Image.new('RGB', (self.tmux.width, self.tmux.height), BG_COLOR)
        if not clean:
            cover = {
                'image': lyvi.md.cover, 
                'pane': self.tmux.layout[lyvi.config['bg_tmux_cover_pane'] + 1],
                'underlying': lyvi.config['bg_tmux_cover_underlying']
            }
            backdrops = {
                'image': lyvi.md.backdrops, 
                'pane': self.tmux.layout[lyvi.config['bg_tmux_backdrops_pane'] + 1],
                'underlying': lyvi.config['bg_tmux_backdrops_underlying']
            }
            if lyvi.config['bg_tmux_backdrops_pane'] == lyvi.config['bg_tmux_cover_pane']:
                to_paste = [cover if self.type == 'cover' else backdrops]
            else:
                to_paste = [cover, backdrops]
            for t in (t for t in to_paste if t['image']):
                t['image'] = resize(t['image'], t['pane'].w * self.tmux.cell.w,
                                                t['pane'].h * self.tmux.cell.h)
                if t['underlying']:
                    t['image'] = blend(t['image'], self.opacity)
                x1 = t['pane'].x * self.tmux.cell.w
                y1 = t['pane'].y * self.tmux.cell.h
                x2 = (t['pane'].x + t['pane'].w) * self.tmux.cell.w
                y2 = (t['pane'].y + t['pane'].h) * self.tmux.cell.h
                x = round(x1 + (x2 - x1) / 2 - t['image'].size[0] / 2)
                y = round(y1 + (y2 - y1) / 2 - t['image'].size[1] / 2)
                image = paste(image, t['image'], x, y)
        image.save(self.file)
