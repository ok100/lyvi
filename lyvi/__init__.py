# Copyright (c) 2013 Ondrej Kipila <ok100 at lavabit dot com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os
import runpy
import sys
from threading import Lock

import lyvi.utils


VERSION = '2.0-git'
USERAGENT = 'lyvi/%s' % VERSION
TEMP = '/tmp'
PID = os.getpid()

# Parse command-line args
args = lyvi.utils.parse_args()

# Default settings
config = {
    'mpd_config_file': os.environ['HOME'] + '/.mpdconf'
        if os.path.exists(os.environ['HOME'] + '/.mpdconf') else '/etc/mpd.conf',
    'mpd_host': os.environ['MPD_HOST'] if 'MPD_HOST' in os.environ else 'localhost',
    'mpd_port': os.environ['MPD_PORT'] if 'MPD_PORT' in os.environ else 6600,
    'default_view': 'lyrics',
    'header_bg': 'default',
    'header_fg': 'white',
    'text_bg': 'default',
    'text_fg': 'default',
    'statusbar_bg': 'default',
    'statusbar_fg': 'default',
    'key_quit': 'q',
    'key_toggle_views': 'a',
    'key_reload_view': 'R',
    'key_toggle_bg_type': 's',
    'bg': False,
    'bg_tmux': False,
    'bg_type': 'cover',
    'bg_opacity': 0.15,
}

# Read configuration file
config_file = args.config_file or '%s/.config/lyvi/lyvi.conf' % os.environ['HOME']
if os.path.exists(config_file):
    config.update((k, v) for k, v in runpy.run_path(config_file).items() if k in config)
else:
    print('File not found: %s' % config_file)
    sys.exit()

if lyvi.args.version:
    # Print version and exit
    import plyr
    print('Lyvi %s, using libglyr %s' % (lyvi.VERSION, plyr.version().split()[1]))
    sys.exit()

import lyvi.players
if lyvi.args.list_players:
    # Print a list of supported players and exit
    import inspect
    print('\033[1mSupported players:\033[0m')
    for name, obj in inspect.getmembers(lyvi.players):
        if inspect.ismodule(obj):
            print('* %s' % name)
    sys.exit()
# TODO: autodetection
player = lyvi.players.mpd.Player()
if lyvi.args.command:
    # TODO: send a command to the connected player and exit
    sys.exit()

# Set up background
if config['bg']:
    import lyvi.background
    bg = lyvi.background.Background()
    tmux = lyvi.background.Tmux() if 'TMUX' in os.environ else None
else:
    bg = None

# Set up UI
import lyvi.ui
lock = Lock()
ui = lyvi.ui.Ui()

from lyvi.main import main
