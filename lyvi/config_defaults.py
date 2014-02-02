# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

"""Default configuration options."""


import os


defaults = {
# Enable autoscroll.
# Type: bool
# Default value: False
'autoscroll': False,

# Enable background. Currently, the background is supported only in urxvt.
# Type: bool
# Default value: False
'bg': False,

# Background opacity.
# Type: float
# Default value: 0.15
'bg_opacity': 0.15,

# A tmux pane where the backdrops are displayed. Panes are numbered from 0.
# To enable tmux support, this option must be set.
# Type: int
# Default value: None
'bg_tmux_backdrops_pane': None,

# Set to True if Lyvi is running in the same pane where backdrops are displayed.
# Type: bool
# Default value: False
'bg_tmux_backdrops_underlying': False,

# A tmux pane where the covers are displayed. Panes are numbered from 0.
# To enable tmux support, this option must be set.
# Type: int
# Default value: None
'bg_tmux_cover_pane': None,

# Set to True if Lyvi is running in the same pane where covers are displayed.
# Type: bool
# Default value: False
'bg_tmux_cover_underlying': False,

# A title of the terminal window running tmux.
# To enable tmux support, this option must be set.
# Type: str
# Default value: None
'bg_tmux_window_title': None,

# Default background type.
# Type: 'cover', 'backdrops'
# Default value: 'cover'
'bg_type': 'cover',

# Try to find player specified with this option first.
# Type: str
# Default value: None
'default_player': None,

# Default view.
# Type: 'lyrics', 'artistbio', 'guitartabs'
# Default value: 'lyrics'
'default_view': 'lyrics',

# Background color of the header.
# Type: str
# Default value: 'default'
'header_bg': 'default',

# Foreground color of the header.
# Type: str
# Default value: 'white'
'header_fg': 'white',

# 'Quit' key.
# Type: str
# Default value: 'q'
'key_quit': 'q',

# 'Reload background' key.
# Type: str
# Default value: 'R'
'key_reload_bg': 'R',

# 'Reload current view' key.
# Type: str
# Default value: 'r'
'key_reload_view': 'r',

# 'Toggle background type' key.
# Type: str
# Default value: 's'
'key_toggle_bg_type': 's',

# 'Toggle view' key.
# Type: str
# Default value: 'a'
'key_toggle_views': 'a',

# 'Toggle UI' key.
# Type: str
# Default value: 'h'
'key_toggle_ui': 'h',

# Path to the mpd configuration file.
# Type: str
# Default value: '~/.mpdconf' or '/etc/mpd.conf'
'mpd_config_file': os.path.join(os.environ['HOME'], '.mpdconf')
    if os.path.exists(os.path.join(os.environ['HOME'], '.mpdconf')) else '/etc/mpd.conf',

# Mpd host.
# Type: str
# Default value: same as MPD_HOST environment variable or 'localhost'
'mpd_host': os.environ['MPD_HOST'] if 'MPD_HOST' in os.environ else 'localhost',

# Mpd port.
# Type: int
# Default value: same as MPD_PORT environment variable or 6600
'mpd_port': os.environ['MPD_PORT'] if 'MPD_PORT' in os.environ else 6600,

# Path to the mplayer configuration directory.
# Type: str
# Default value: '~/.mplayer'
'mplayer_config_dir': os.path.join(os.environ['HOME'], '.mplayer'),

# Path to the saved cover.
# Type: str
# Default value: None
'save_cover': None,

# Path to the saved lyrics.
# Type: str
# Default value: None
'save_lyrics': None,

# Background color of the statusbar.
# Type: str
# Default value: 'default'
'statusbar_bg': 'default',

# Foreground color of the statusbar.
# Type: str
# Default value: 'default'
'statusbar_fg': 'default',

# Background color of the text.
# Type: str
# Default value: 'default'
'text_bg': 'default',

# Foreground color of the text.
# Type: str
# Default value: 'default'
'text_fg': 'default',

# Hide UI by default.
# Type: bool
# Default value: False
'ui_hidden': False,
}
