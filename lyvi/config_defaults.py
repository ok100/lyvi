# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os

defaults = {
    'bg': False,
    'bg_opacity': 0.15,
    'bg_tmux_backdrops_pane': None,
    'bg_tmux_backdrops_underlying': False,
    'bg_tmux_cover_pane': None,
    'bg_tmux_cover_underlying': False,
    'bg_tmux_window_title': None,
    'bg_type': 'cover',
    'default_player': None,
    'default_view': 'lyrics',
    'header_bg': 'default',
    'header_fg': 'white',
    'key_quit': 'q',
    'key_reload_view': 'R',
    'key_toggle_bg_type': 's',
    'key_toggle_views': 'a',
    'key_hide_ui': 'h',
    'mpd_config_file': os.environ['HOME'] + '/.mpdconf'
        if os.path.exists(os.environ['HOME'] + '/.mpdconf') else '/etc/mpd.conf',
    'mpd_host': os.environ['MPD_HOST'] if 'MPD_HOST' in os.environ else 'localhost',
    'mpd_port': os.environ['MPD_PORT'] if 'MPD_PORT' in os.environ else 6600,
    'save_cover': False,
    'save_cover_filename': '<songdir>/cover.jpg',
    'save_lyrics': False,
    'save_lyrics_filename': '<songdir>/<filename>.lyric',
    'statusbar_bg': 'default',
    'statusbar_fg': 'default',
    'ui_hidden': False,
    'text_bg': 'default',
    'text_fg': 'default',
}
