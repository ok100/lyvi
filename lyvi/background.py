# Copyright (c) 2013 Ondrej Kipila <ok100 at lavabit dot com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os
from io import BytesIO

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


class Tmux:
    def get_layout(self):
        class Pane: pass
        display = get_output('tmux display -p \'#{window_layout}\'')
        for delim in '[]{}':
            display = display.replace(delim, ',')
        self.layout = [Pane()]
        self.layout[0].x, self.layout[0].y = (int(a) for a in display.split(',')[1].split('x'))
        display = display.split(',', 1)[1]
        chunks = display.split(',')
        for i in range(0, len(chunks) - 1):
            if 'x' in chunks[i] and 'x' not in chunks[i + 3]:
                self.layout.append(Pane())
                self.layout[-1].x, self.layout[-1].y = (int(a) for a in chunks[i].split('x'))
                self.layout[-1].x_offset = int(chunks[i + 1])
                self.layout[-1].y_offset = int(chunks[i + 2])
        lsp = get_output('tmux lsp').splitlines()
        for chunk in lsp:
            self.layout[lsp.index(chunk) + 1].active = 'active' in chunk
