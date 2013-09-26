# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
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
        if key == 'j':
            self.keypress(size, 'down')
            return True
        if key == 'k':
            self.keypress(size, 'up')
            return True
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
    view = lyvi.config['default_view']
    hidden = lyvi.config['ui_hidden']
    _header = ''
    _text = ''
    quit = False

    @property
    def header(self):
        return self._header

    @property
    def text(self):
        return self._text

    @header.setter
    def header(self, value):
        self._header = value
        if not self.hidden:
            self.head.set_text(('header', self.header))

    @text.setter
    def text(self, value):
        self._text = value
        if not self.hidden:
            self.content[:] = [self.head, urwid.Divider()] + \
                [urwid.Text(('content', line)) for line in self.text.splitlines()]

    def init(self):
        palette = [
            ('header', lyvi.config['header_fg'], lyvi.config['header_bg']),
            ('content', lyvi.config['text_fg'], lyvi.config['text_bg']),
            ('statusbar', lyvi.config['statusbar_fg'], lyvi.config['statusbar_bg']),
        ]
        self.head = urwid.Text(('header', ''))
        self.statusbar = urwid.AttrMap(urwid.Text('', align='right'), 'statusbar')
        self.content = urwid.SimpleListWalker([urwid.Text(('content', ''))])
        self.listbox = MyListBox(self.content)
        self.frame = urwid.Frame(urwid.Padding(self.listbox, left=1, right=1),
            footer=self.statusbar)
        urwid.connect_signal(self.listbox, 'changed', self.update_statusbar)
        self.loop = urwid.MainLoop(self.frame, palette, unhandled_input=self.input)
        self.set_alarm()

    def set_alarm(self):
        self.loop.event_loop.alarm(0.5, self.check_exit)

    def update(self):
        if lyvi.player.state == 'stop':
            self.header = 'N/A' if self.view == 'artistbio' else 'N/A - N/A'
            self.text = 'Not playing'
        elif self.view == 'lyrics':
            self.header = '%s - %s' % (lyvi.md.artist or 'N/A', lyvi.md.title or 'N/A')
            self.text = lyvi.md.lyrics or 'No lyrics found'
        elif self.view == 'artistbio':
            self.header = lyvi.md.artist or 'N/A'
            self.text = lyvi.md.artistbio or 'No artist info found'
        elif self.view == 'guitartabs':
            self.header = '%s - %s' % (lyvi.md.artist or 'N/A', lyvi.md.title or 'N/A')
            self.text = lyvi.md.guitartabs or 'No guitar tabs found'
        self.refresh()

    def refresh(self):
        self.loop.draw_screen()

    def home(self):
        """Scroll to the top of the current view"""
        self.listbox.set_focus(0)
        self.refresh()

    def update_statusbar(self, x=None):
        if not self.hidden:
            text = urwid.Text(self.view + self.listbox.pos.rjust(10), align='right')
            wrap = urwid.AttrWrap(text, 'statusbar')
            self.frame.set_footer(wrap)

    def toggle_views(self, x=None):
        """Toggle between views"""
        if not self.hidden:
            views = ['lyrics', 'artistbio', 'guitartabs']
            n = views.index(self.view)
            self.view = views[n + 1] if n < len(views) - 1 else views[0]
            self.home()
            self.update()

    def toggle_visibility(self):
        if lyvi.bg:
            if not self.hidden:
                self.header = ''
                self.text = ''
                self.frame.set_footer(urwid.AttrWrap(urwid.Text(''), 'statusbar'))
                lyvi.bg.opacity = 1.0
                lyvi.bg.update()
                self.hidden = True
            else:
                self.hidden = False
                lyvi.bg.opacity = lyvi.config['bg_opacity']
                lyvi.bg.update()
                self.update()

    def reload_view(self):
        """Reload current view"""
        from lyvi.utils import thread
        import lyvi.metadata
        lyvi.md.delete(self.view, lyvi.md.artist, lyvi.md.title, lyvi.md.album)
        thread(lyvi.md.get, (self.view,))

    def input(self, key):
        bindings = {
            lyvi.config['key_quit']: lyvi.exit,
            lyvi.config['key_toggle_views']: self.toggle_views,
            lyvi.config['key_reload_view']: self.reload_view,
            lyvi.config['key_toggle_bg_type']: lyvi.bg.toggle_type if lyvi.bg else None,
            lyvi.config['key_hide_ui']: self.toggle_visibility,
        }
        if key in bindings:
            bindings[key]()

    def mainloop(self):
        """Start the main loop"""
        self.loop.run()

    def check_exit(self):
        self.set_alarm()
        if self.quit:
            raise urwid.ExitMainLoop()
