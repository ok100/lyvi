# Copyright (c) 2013 Ondrej Kipila <ok100 at lavabit dot com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import urwid

import lyvi


class MyListBox(urwid.ListBox):
    signals = ['changed']

    def mouse_event(self, size, event, button, col, row, focus):
        if event == 'mouse press':
            if button == 4:
                self.keypress(size, 'up')
                return True
            if button == 5:
                self.keypress(size, 'down')
                return True
        return self.__super.mouse_event(size, event, button, col, row, focus)

    def keypress(self, size, key):
        if key == 'g':
            self.set_focus(0)
            return True
        if key == 'G':
            self.set_focus(len(self.body) - 1)
            self.set_focus_valign('bottom')
            return True
        return self.__super.keypress(size, key)

    def calculate_visible(self, size, focus=False):
        width, height = size
        middle, top, bottom = self.__super.calculate_visible(size, focus)
        fpos = self.body.index(top[1][-1][0]) if top[1] else self.focus_position
        top_line = sum([self.body[n].rows((width,)) for n in range(0, fpos)]) + top[0]
        total_lines = sum([widget.rows((width,)) for widget in self.body])
        if total_lines <= height:
            self.pos = 'All'
        elif top_line == 0:
            self.pos = 'Top'
        elif top_line + height == total_lines:
            self.pos = 'Bot'
        else:
            self.pos = '%d%%' % round(top_line * 100 / (total_lines - height))
        self._emit('changed')
        return middle, top, bottom


class Ui:
    def init(self):
        self.views = ['lyrics', 'artistbio', 'guitartabs']
        for view in self.views:
            setattr(self, view, None)
        self.artist = None
        self.title = None
        self.view = 'lyrics'

        self.header = urwid.Text(('header', ''))
        self.statusbar = urwid.Text(('statusbar', ''), align='right')
        self.content = urwid.SimpleListWalker([urwid.Text(('content', ''))])
        self.listbox = MyListBox(self.content)

        palette = [
            ('header', 'white', ''),
            ('content', '', ''),
            ('statusbar', '', ''),
        ]
        view = urwid.Frame(urwid.Padding(self.listbox, left=1, right=1),
            footer=self.statusbar)

        urwid.connect_signal(self.listbox, 'changed', self.update_statusbar)

        self.loop = urwid.MainLoop(view, palette, unhandled_input=self.input)
        self.update()

    def set_header(self, header):
        self.header.set_text(('header', header))

    def set_text(self, text):
        self.content[:] = [self.header, urwid.Divider()] + \
            [urwid.Text(('content', line)) for line in text.splitlines()]

    def update(self):
        if lyvi.player.status == 'stopped':
            self.set_header('N/A' if self.view == 'artistbio' else 'N/A - N/A')
            self.set_text('Not playing')
        elif self.view == 'lyrics':
            self.set_header('%s - %s' % (self.artist or 'N/A', self.title or 'N/A'))
            self.set_text(self.lyrics or 'No lyrics found')
        elif self.view == 'artistbio':
            self.set_header(self.artist or 'N/A')
            self.set_text(self.artistbio or 'No artist info found')
        elif self.view == 'guitartabs':
            self.set_header('%s - %s' % (self.artist or 'N/A', self.title or 'N/A'))
            self.set_text(self.guitartabs or 'No guitar tabs found')
        self.refresh()

    def refresh(self):
        self.loop.draw_screen()

    def home(self):
        self.listbox.set_focus(0)
        self.refresh()

    def update_statusbar(self, x=None):
        self.statusbar.set_text(('statusbar',
            '%s%s' % (self.view, self.listbox.pos.rjust(10))))

    def toggle_views(self, x=None):
        n = self.views.index(self.view)
        self.view = self.views[n + 1] if n < len(self.views) - 1 else self.views[0]
        self.home()
        self.update()

    def input(self, key):
        if key in ('q', 'Q'):
            # Quit
            self.exit()
        elif key == 'a':
            # Toggle between views
            self.toggle_views()
        elif key == 'R':
            # Reload current view
            # FIXME
            from threading import Thread
            import lyvi.glyr
            self.home()
            text = 'Searching %s...' % \
                ('artist info' if self.view == 'artistbio' else
                'guitar tabs' if self.view == 'guitartabs' else self.view)
            setattr(self, self.view, text)
            self.update()
            lyvi.glyr.cache_delete(self.artist, self.title)
            worker = Thread(target=lyvi.glyr.get_and_update,
                                   args=(self.view, self.artist, self.title))
            worker.daemon = True
            worker.start()

    def exit(self):
        raise urwid.ExitMainLoop()
