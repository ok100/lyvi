# Copyright (c) 2013 Ondrej Kipila <ok100 at lavabit dot com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os
from io import BytesIO
from threading import Lock

import Image

import lyvi
from lyvi.metadata import get
from lyvi.utils import check_output


if 'TMUX' in os.environ:
    BG_BEG = 'printf "\ePtmux;\e\e]20;'   
    BG_END = ';100x100+50+50:op=keep-aspect\a\e\\\\"'
else:
    BG_BEG = 'printf "\e]20;'
    BG_END = ';100x100+50+50:op=keep-aspect\a"'
for line in check_output('xrdb -query').splitlines():
    if 'background' in line:
        BG_COLOR = line.split(':')[1].strip()


class Background:
    def __init__(self):
        self.lock = Lock()
        self.reset_tags()
        self.backdrops = self.cover = None
        self.type = lyvi.config['bg_type']
        self.opacity = lyvi.config['bg_opacity']
        self.file = '%s/lyvi-%s.jpg' % (lyvi.TEMP, lyvi.PID)

    def set_tags(self):
        self.artist = lyvi.player.artist
        self.title = lyvi.player.title
        self.album = lyvi.player.album

    def reset_tags(self):
        self.artist = self.title = self.album = None

    def toggle_type(self):
        self.type = 'cover' if self.type == 'backdrops' else 'backdrops'
        with self.lock:
            self.update()

    def blend(self, image, opacity):
        buf = BytesIO(image)
        image = Image.open(buf)
        layer = Image.new(image.mode, image.size, BG_COLOR)
        return Image.blend(image, layer, 1 - opacity)

    def update(self):
        if ((self.type == 'backdrops' and self.backdrops and self.artist)
                or (self.type == 'cover' and self.cover and self.album)):
            self.blend(getattr(self, self.type), self.opacity).save(self.file, format="JPEG")
        else:
            # Create empty image
            image = Image.new('RGB', (100, 100), BG_COLOR)
            image.save(self.file)
        # Set the image as background
        os.system(BG_BEG + self.file + BG_END)

    def cleanup(self):
        self.reset_tags()
        with self.lock:
            self.update()
        os.remove(self.file)


class Tmux:
    def get_layout(self):
        class Pane:
            pass
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
