# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

"""Curses user interface."""


from math import ceil
from time import sleep
from threading import Thread, Event

import urwid

import lyvi


class VimListBox(urwid.ListBox):
    """A ListBox subclass which provides vim-like and mouse scrolling.

    Additional properties:
    size -- a tuple (width, height) of the listbox dimensions
    total_lines -- total number of lines
    pos -- a string containing vim-like scroll position indicator

    Additional signals:
    changed -- emited when the listbox content changes
    """
    signals = ['changed']

    def mouse_event(self, size, event, button, col, row, focus):
        """Overrides ListBox.mouse_event method.

        Implements mouse scrolling.
        """
        if event == 'mouse press':
            if button == 4:
                for _ in range(3):
                    self.keypress(size, 'up')
                return True
            if button == 5:
                for _ in range(3):
                    self.keypress(size, 'down')
                return True
        return self.__super.mouse_event(size, event, button, col, row, focus)

    def keypress(self, size, key):
        """Overrides ListBox.keypress method.

        Implements vim-like scrolling.
        """
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
        """Overrides ListBox.calculate_visible method.

        Calculates the scroll position (like in vim).
        """
        self.size = size
        width, height = size
        middle, top, bottom = self.__super.calculate_visible(self.size, focus)
        fpos = self.body.index(top[1][-1][0]) if top[1] else self.focus_position
        top_line = sum([self.body[n].rows((width,)) for n in range(0, fpos)]) + top[0]
        self.total_lines = sum([widget.rows((width,)) for widget in self.body])
        if self.total_lines <= height:
            self.pos = 'All'
        elif top_line == 0:
            self.pos = 'Top'
        elif top_line + height == self.total_lines:
            self.pos = 'Bot'
        else:
            self.pos = '%d%%' % round(top_line * 100 / (self.total_lines - height))
        self._emit('changed')
        return middle, top, bottom


class Autoscroll(Thread):
    """A Thread subclass that implements autoscroll timer."""
    def __init__(self, widget):
        """Initialize the class."""
        super().__init__()
        self.daemon = True
        self.widget = widget
        self.event = Event()

    def _can_scroll(self):
        """Return True if we can autoscroll."""
        return (lyvi.player.length and lyvi.player.state == 'play' and lyvi.ui.view == 'lyrics'
                and not lyvi.ui.hidden and self.widget.pos not in ('All', 'Bot'))

    def run(self):
        """Start the timer."""
        while True:
            if self._can_scroll():
                time = ceil(lyvi.player.length / (self.widget.total_lines - self.widget.size[1]))
                reset = False
                for _ in range(time):
                    if self.event.wait(1):
                        reset = True
                        self.event.clear()
                        break
                if not reset and self._can_scroll():
                    self.widget.keypress(self.widget.size, 'down')
            else:
                sleep(1)

    def reset(self):
        """Reset the timer."""
        self.event.set()


class Ui:
    """Main UI class.

    Attributes:
    view -- current view
    hidden -- whether the UI is hidden
    quit -- stop the mainloop if this flag is set to True
    """
    view = lyvi.config['default_view']
    hidden = lyvi.config['ui_hidden']
    _header = ''
    _text = ''
    quit = False

    @property
    def header(self):
        """Header text."""
        return self._header

    @header.setter
    def header(self, value):
        self._header = value
        if not self.hidden:
            self.head.set_text(('header', self.header))
            self._refresh()

    @property
    def text(self):
        """The main text."""
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        if not self.hidden:
            lines = [urwid.Text(('content', line)) for line in self.text.splitlines()]
            self.content[:] = [self.head, urwid.Divider()] + lines
            self._refresh()

    def init(self):
        """Initialize the class."""
        palette = [
            ('header', lyvi.config['header_fg'], lyvi.config['header_bg']),
            ('content', lyvi.config['text_fg'], lyvi.config['text_bg']),
            ('statusbar', lyvi.config['statusbar_fg'], lyvi.config['statusbar_bg']),
        ]

        self.head = urwid.Text(('header', ''))
        self.statusbar = urwid.AttrMap(urwid.Text('', align='right'), 'statusbar')
        self.content = urwid.SimpleListWalker([urwid.Text(('content', ''))])
        self.listbox = VimListBox(self.content)
        self.frame = urwid.Frame(urwid.Padding(self.listbox, left=1, right=1), footer=self.statusbar)
        self.loop = urwid.MainLoop(self.frame, palette, unhandled_input=self.input)
        self.autoscroll = Autoscroll(self.listbox) if lyvi.config['autoscroll'] else None

        if self.autoscroll:
            self.autoscroll.start()
        urwid.connect_signal(self.listbox, 'changed', self.update_statusbar)
        self._set_alarm()

    def update(self):
        """Update the listbox content."""
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

    def home(self):
        """Scroll to the top of the current view."""
        self.listbox.set_focus(0)
        self._refresh()

    def update_statusbar(self, _=None):
        """Update the statusbar.

        Arguments are ignored, but enable support for urwid signal callback.
        """
        if not self.hidden:
            text = urwid.Text(self.view + self.listbox.pos.rjust(10), align='right')
            wrap = urwid.AttrWrap(text, 'statusbar')
            self.frame.set_footer(wrap)

    def toggle_views(self):
        """Toggle between views."""
        if not self.hidden:
            views = ['lyrics', 'artistbio', 'guitartabs']
            n = views.index(self.view)
            self.view = views[n + 1] if n < len(views) - 1 else views[0]
            self.home()
            self.update()

    def toggle_visibility(self):
        """Toggle UI visibility."""
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

    def reload(self, type):
        """Reload metadata for current view."""
        from lyvi.utils import thread
        import lyvi.metadata
        lyvi.md.delete(type, lyvi.md.artist, lyvi.md.title, lyvi.md.album)
        thread(lyvi.md.get, (type,))

    def input(self, key):
        """Process input not handled by any widget."""
        if key == lyvi.config['key_quit']:
            lyvi.exit()
        elif key == lyvi.config['key_toggle_views']:
            self.toggle_views()
        elif key == lyvi.config['key_reload_view']:
            self.reload(self.view)
        elif key == lyvi.config['key_reload_bg'] and lyvi.bg:
            self.reload(lyvi.bg.type)
        elif key == lyvi.config['key_toggle_bg_type'] and lyvi.bg:
            lyvi.bg.toggle_type()
        elif key == lyvi.config['key_toggle_ui']:
            self.toggle_visibility()

    def mainloop(self):
        """Start the mainloop."""
        self.loop.run()

    def _set_alarm(self):
        """Set the alarm for _check_exit."""
        self.loop.event_loop.alarm(0.5, self._check_exit)

    def _check_exit(self):
        """Stop the mainloop if the quit property is True."""
        self._set_alarm()
        if self.quit:
            raise urwid.ExitMainLoop()

    def _refresh(self):
        """Redraw the screen."""
        self.loop.draw_screen()
