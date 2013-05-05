# Copyright (c) 2013 Ondrej Kipila <ok100 at lavabit dot com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import textwrap

import termbox

import lyvi


COLORS = {
    'default': 0x0F,
    'black': termbox.BLACK,
    'red': termbox.RED,
    'green': termbox.GREEN,
    'yellow': termbox.YELLOW,
    'blue': termbox.BLUE,
    'magenta': termbox.MAGENTA,
    'cyan': termbox.CYAN,
    'white': termbox.WHITE,
}
HEADER_BG = COLORS[lyvi.config['header_bg']]
HEADER_FG = COLORS[lyvi.config['header_fg']]
TEXT_BG = COLORS[lyvi.config['text_bg']]
TEXT_FG = COLORS[lyvi.config['text_fg']]
STATUSBAR_BG = COLORS[lyvi.config['statusbar_bg']]
STATUSBAR_FG = COLORS[lyvi.config['statusbar_fg']]


class Ui(termbox.Termbox):
    def __init__(self):
        self.artist = self.title = self.lyrics = self.artistbio = self.guitartabs = None
        self.quit = False
        self.playing = False
        self.pos_y = 0

    def init(self):
        """Init the terminal.
        """
        termbox.Termbox.__init__(self)

    def puts(self, x, y, string, fg, bg):
        """Write string at start position (x; y).
        """
        for char in string:
            self.change_cell(x, y, ord(char), fg, bg)
            x += 1

    def set_view(self, view):
        """Set the view - lyrics, artistbio, guitartabs.
        """
        self.view = view
        if view == 'lyrics':
            self.header = '%s - %s' % (self.artist if self.artist else 'N/A',
                                       self.title if self.title else 'N/A')
            self.text = ((self.lyrics if self.lyrics else 'No lyrics found.')
                          if self.artist and self.title else 'Missing tags.') if self.playing else 'Not playing.'
        elif view == 'artistbio':
            self.header = self.artist if self.artist else 'N/A'
            self.text = ((self.artistbio if self.artistbio else 'No artist info found.')
                          if self.artist else 'Missing tags.') if self.playing else 'Not playing.'
        elif view == 'guitartabs':
            self.header = '%s - %s' % (self.artist if self.artist else 'N/A',
                                       self.title if self.title else 'N/A')
            self.text = ((self.guitartabs if self.guitartabs else 'No guitar tabs found.')
                          if self.artist and self.title else 'Missing tags.') if self.playing else 'Not playing.'

    def toggle_views(self):
        """Toggle between views.
        """
        self.pos_y = 0
        views = ['lyrics', 'artistbio', 'guitartabs']
        self.set_view(views[views.index(self.view) + 1] if views.index(self.view) + 1 < len(views) else views[0])
        self.refresh()

    def wrap(self):
        """Wrap the content of self.text and self.header
           and store it into self.content array.
        """
        self.content = []

        for wrapped_line in textwrap.wrap(self.header, self.width() - 2):
            self.content.append(wrapped_line)
        self.content.append(-1)
        for line in self.text.strip().splitlines():
            if line == '':
                self.content.append('')
            else:
                for wrapped_line in textwrap.wrap(line, self.width() - 2, replace_whitespace=False):
                    self.content.append(wrapped_line)

    def refresh(self):
        """Refresh the UI.
        """
        self.set_view(self.view)
        self.wrap()
        self.redraw()


    def redraw(self):
        """Redraw the UI.
        """
        self.clear()

        # Update pager text
        y = 0
        view = self.content[self.pos_y:self.pos_y + self.height() - 1]
        if -1 in view:
            bg = HEADER_BG
            fg = HEADER_FG | termbox.BOLD
        else:
            bg = TEXT_BG
            fg = TEXT_FG
        view += (self.height() - len(view) - 1) * ['']
        for line in view:
            if line == -1:
                bg = TEXT_BG
                fg = TEXT_FG
                line = ''
            self.puts(0, y, ' ' + line.ljust(self.width() - 1), fg, bg)
            y += 1

        # Calculate position
        if len(self.content) <= self.height() - 1:
            pos = 'All'
        elif self.pos_y == 0:
            pos = 'Top'
        elif self.pos_y >= len(self.content) - self.height() + 1:
            pos = 'Bot'
        else:
            pos = '%d%%' % round(self.pos_y * 100 / (len(self.content) - self.height() + 1))
        pos = pos.rjust(4)

        # Update statusbar
        statustext = '%s    %s' % (self.view, pos)

        self.puts(0, self.height() - 1, statustext.rjust(self.width()), STATUSBAR_FG, STATUSBAR_BG)
        self.present()

    def mainloop(self):
        """Handle input events.
        """
        self.set_view(lyvi.config['default_view'])
        self.refresh()

        while True:
            type, char, key, mod, width, height = self.poll_event()

            if type == termbox.EVENT_KEY:
                if char == 'q':
                    # Quit
                    self.quit = True
                    break
                elif key == termbox.KEY_ARROW_UP or char == 'k':
                    # Scroll one line up
                    if self.pos_y > 0:
                        self.pos_y -= 1
                elif key == termbox.KEY_ARROW_DOWN or char == 'j':
                    # Scroll one line down
                    if self.pos_y < len(self.content) - self.height() + 1:
                        self.pos_y += 1
                elif key == termbox.KEY_PGUP or key == termbox.KEY_ARROW_LEFT:
                    # Scroll one page up
                    self.pos_y -= self.height() - 1
                    if self.pos_y < 0:
                        self.pos_y = 0
                elif key == termbox.KEY_PGDN or key == termbox.KEY_ARROW_RIGHT:
                    # Scroll one page down
                    if self.pos_y < len(self.content) - self.height() + 1:
                        self.pos_y += self.height() - 1
                elif char == 'g':
                    # Scroll to top
                    self.pos_y = 0
                elif char == 'G':
                    # Scroll to bottom
                    self.pos_y = len(self.content) - self.height() + 1
                elif char == 'a':
                    # Toggle view
                    self.toggle_views()

            elif type == termbox.EVENT_RESIZE:
                self.refresh()

            self.redraw()
