# Copyright (c) 2013 Ondrej Kipila <ok100 at lavabit dot com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os
from io import BytesIO

import Image

import lyvi
import lyvi.glyr
from lyvi.utils import check_output


class Background:
    def __init__(self):
        self.artist = self.title = self.album = None
        self.backdrops = self.cover = None
        self.type = lyvi.config['bg_type']
        self.is_set = False
        for line in check_output('xrdb -query').splitlines():
            if 'background' in line:
                self.bg_color = line.split(':')[1].strip()

    def toggle_type(self):
        self.type = 'cover' if self.type == 'backdrops' else 'backdrops'
        self.update()

    def update(self):
        setattr(self, self.type, lyvi.glyr.get(self.type, self.artist, self.title, self.album))
        self.set()

    def set(self, opacity=lyvi.config['bg_opacity']):
        if not getattr(self, self.type):
            self.unset()
            return

        file = '%s/lyvi-%s-tmp' % (lyvi.TEMP, lyvi.PID)
        with open(file, 'wb') as buf:
            buf.write(getattr(self, self.type))
        image1 = Image.open(file)
        layer = Image.new(image1.mode, image1.size, self.bg_color)
        image2 = Image.blend(image1, layer, 1 - opacity)
        buf = BytesIO()
        image2.save(buf, format="JPEG")
        img = buf.getvalue()
        file = '%s/lyvi-%s-%s.png' % (lyvi.TEMP, lyvi.PID, self.type)
        with open(file, 'wb') as f:
            f.write(img)

        if lyvi.tmux:
            os.system('printf "\ePtmux;\e\e]20;%s;100x100+50+50:op=keep-aspect\a\e\\\\"' % file)
        else:
            os.system('printf "\e]20;%s;100x100+50+50:op=keep-aspect\a"' % file)
        self.is_set = True

    def unset(self):
        if not self.is_set:
            return
        file = '%s/lyvi-%s-blank.png' % (lyvi.TEMP, lyvi.PID)
        if not os.path.exists(file):
            image = Image.new('RGB', (100, 100), self.bg_color)
            image.save(file)
        if lyvi.tmux:
            os.system('printf "\ePtmux;\e\e]20;%s\a\e\\\\"' % file)
        else:
            os.system('printf "\e]20;%s\a"' % file)
        self.artist = self.title = self.album = None
        self.is_set = False


class Tmux:
    def get_layout(self):
        class TmuxPane:
            pass
        display = get_output('tmux display -p \'#{window_layout}\'')
        lsp = get_output('tmux lsp')
        for delim in '[]{}':
            display = display.replace(delim, ',')
        self.layout = [TmuxPane()]
        self.layout[0].x, self.layout[0].y = [int(a) for a in display.split(',')[1].split('x')]
        display = display.split(',', 1)[1]
        chunks = display.split(',')
        for i in range(0, len(chunks) - 1):
            if 'x' in chunks[i] and 'x' not in chunks[i + 3]:
                self.layout.append(TmuxPane())
                self.layout[-1].x, self.layout[-1].y = [int(a) for a in chunks[i].split('x')]
                self.layout[-1].x_offset = int(chunks[i + 1])
                self.layout[-1].y_offset = int(chunks[i + 2])
        for c in lsp.splitlines():
            self.layout[lsp.splitlines().index(c) + 1].active = True if 'active' in c else False
