# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

"""Classes for normal and Tmux backgrounds."""


import os
import sys
from io import BytesIO

from PIL import Image

import lyvi
from lyvi.utils import check_output


# Get the terminal background color from the 'xrdb' command
for line in check_output('xrdb -query').splitlines():
    if 'background' in line:
        BG_COLOR = line.split(':')[1].strip()
        break
else:
    BG_COLOR = '#FFFFFF'


def pil_image(image):
    """Return the initialized Image class.

    Keyword arguments:
    image -- bytes or Image instance
    """
    if isinstance(image, bytes):
        buf = BytesIO(image)
        return Image.open(buf)
    return image


def blend(image, opacity):
    """Return the image blended with terminal background color.

    Keyword arguments:
    image -- image to blend
    opacity -- opacity of the background color layer
    """
    image = pil_image(image)
    layer = Image.new(image.mode, image.size, BG_COLOR)
    return Image.blend(image, layer, 1 - opacity)


def paste(root, image_to_paste, x, y):
    """Return root image with pasted image.

    Keyword arguments:
    root -- root image
    image_to_paste -- image to paste
    x -- top-left x coordinates of the image to paste
    y -- top-left y coordinates of the image to paste
    """
    root = pil_image(root)
    image_to_paste = pil_image(image_to_paste)
    root.paste(image_to_paste, (x, y))
    return root


def resize(image, x, y):
    """Return the resized image.

    Keyword argumants:
    image -- image to resize
    x -- new x resolution in px
    y -- new y resolution in px
    """
    image = pil_image(image)
    image.thumbnail((x, y), Image.ANTIALIAS)
    return image


class Background:
    ESCAPE_STR_BEG = "\033]20;"
    ESCAPE_STR_END = ";100:op=keep-aspect\a"

    def __init__(self):
        """Initialize the class."""
        self.FILE = os.path.join(lyvi.TEMP, 'lyvi-%s.jpg' % lyvi.PID)
        self.type = lyvi.config['bg_type']
        self.opacity = lyvi.config['bg_opacity']

    def toggle_type(self):
        """Toggle background type."""
        self.type = 'cover' if self.type == 'backdrops' else 'backdrops'
        self.update()

    def _make(self, clean=False):
        """Save the background to a temporary file.

        Keyword arguments:
        clean -- whether the background should be unset
        """
        if (((self.type == 'backdrops' and lyvi.md.backdrops and lyvi.md.artist)
                or (self.type == 'cover' and lyvi.md.cover and lyvi.md.album))
                and not clean):
            image = blend(getattr(lyvi.md, self.type), self.opacity)
        else:
            image = Image.new('RGB', (100, 100), BG_COLOR)
        image.save(self.FILE)

    def _set(self):
        """Set the image file as a terminal background."""
        sys.stdout.write(self.ESCAPE_STR_BEG + self.FILE + self.ESCAPE_STR_END)

    def update(self, clean=False):
        """Update the background.

        Keyword arguments:
        clean -- whether the background should be unset
        """
        self._make(clean=clean)
        self._set()

    def cleanup(self):
        """Unset the background and delete the image file."""
        sys.stdout.write(self.ESCAPE_STR_BEG + ';+1000000\a')
        if os.path.exists(self.FILE):
            os.remove(self.FILE)


class Tmux:
    """A class which represents Tmux layout and dimensions.

    Properties:
    layout -- a list containing Pane instances representing all tmux panes
    width -- window width in px
    height -- window height in px
    cell -- Cell instance representing a terminal cell
    """
    class Cell:
        """Class used as a placeholder for terminal cell properties.

        Properties:
        w -- cell width in px
        h -- cell height in px
        """
        pass

    class Pane:
        """Class used as a placeholder for pane properties.

        Properties:
        active -- whether the pane is active
        x -- horizontal pane offset from the top left corner of the terminal in cells
        y -- vertical pane offset from the top left corner of the terminal in cells
        w -- pane width in cells
        h -- pane height in cells
        """
        pass

    def __init__(self):
        """Initialize the class and update the class properties."""
        self.cell = self.Cell()
        self.update()

    def _get_layout(self):
        """Return a list containing Pane instances representing all tmux panes."""
        display = check_output('tmux display -p \'#{window_layout}\'')
        for delim in '[]{}':
            display = display.replace(delim, ',')
        layout = [self.Pane()]
        layout[0].w, layout[0].h = (int(a) for a in display.split(',')[1].split('x'))
        display = display.split(',', 1)[1]
        chunks = display.split(',')
        for i in range(0, len(chunks) - 1):
            if 'x' in chunks[i] and 'x' not in chunks[i + 3]:
                layout.append(self.Pane())
                layout[-1].w, layout[-1].h = (int(a) for a in chunks[i].split('x'))
                layout[-1].x = int(chunks[i + 1])
                layout[-1].y = int(chunks[i + 2])
        lsp = check_output('tmux lsp').splitlines()
        for chunk in lsp:
            layout[lsp.index(chunk) + 1].active = 'active' in chunk
        return layout

    def _get_size_px(self):
        """Return a tuple (width, height) with the tmux window dimensions in px."""
        while(True):
            # Use xwininfo command to get the window dimensions
            info = check_output('xwininfo -name ' + lyvi.config['bg_tmux_window_title'])
            try:
                width = int(info.split('Width: ')[1].split('\n')[0])
                height = int(info.split('Height: ')[1].split('\n')[0])
            except IndexError:
                continue
            else:
                return width, height

    def update(self):
        """Set class properties to the actual values."""
        self.layout = self._get_layout()
        self.width, self.height = self._get_size_px()
        self.cell.w = round(self.width / self.layout[0].w)
        self.cell.h = round(self.height / self.layout[0].h)


class TmuxBackground(Background):
    ESCAPE_STR_BEG = "\033Ptmux;\033\033]20;"
    ESCAPE_STR_END = ";100x100+50+50:op=keep-aspect\a\033\\\\"

    def __init__(self):
        """Initialize the class."""
        super().__init__()
        self._tmux = Tmux()

    def _make(self, clean=False):
        self._tmux.update()
        image = Image.new('RGB', (self._tmux.width, self._tmux.height), BG_COLOR)
        if not clean:
            cover = {
                'image': lyvi.md.cover,
                'pane': self._tmux.layout[lyvi.config['bg_tmux_cover_pane'] + 1],
                'underlying': lyvi.config['bg_tmux_cover_underlying']
            }
            backdrops = {
                'image': lyvi.md.backdrops,
                'pane': self._tmux.layout[lyvi.config['bg_tmux_backdrops_pane'] + 1],
                'underlying': lyvi.config['bg_tmux_backdrops_underlying']
            }
            if lyvi.config['bg_tmux_backdrops_pane'] == lyvi.config['bg_tmux_cover_pane']:
                to_paste = [cover if self.type == 'cover' else backdrops]
            else:
                to_paste = [cover, backdrops]
            for t in (t for t in to_paste if t['image']):
                t['image'] = resize(t['image'], t['pane'].w * self._tmux.cell.w,
                                    t['pane'].h * self._tmux.cell.h)
                if t['underlying']:
                    t['image'] = blend(t['image'], self.opacity)
                x1 = t['pane'].x * self._tmux.cell.w
                y1 = t['pane'].y * self._tmux.cell.h
                x2 = (t['pane'].x + t['pane'].w) * self._tmux.cell.w
                y2 = (t['pane'].y + t['pane'].h) * self._tmux.cell.h
                x = round(x1 + (x2 - x1) / 2 - t['image'].size[0] / 2)
                y = round(y1 + (y2 - y1) / 2 - t['image'].size[1] / 2)
                image = paste(image, t['image'], x, y)
        image.save(self.FILE)
