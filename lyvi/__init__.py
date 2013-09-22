# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import argparse
import os
import runpy
import sys
from tempfile import gettempdir
from time import sleep

from lyvi.utils import thread


VERSION = '2.0-git'
USERAGENT = 'lyvi/' + VERSION
TEMP = gettempdir()
PID = os.getpid()

# Default settings
config = {
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

# Parse command-line args
parser = argparse.ArgumentParser(prog='lyvi')
parser.add_argument('command', nargs='?',
    help='send a command to the player and exit')
parser.add_argument('-c', '--config-file',
    help='path to an alternate config file')
parser.add_argument('-l', '--list-players',
    help='print a list of supported players and exit', action='store_true')
parser.add_argument('-v', '--version',
    help='print version information and exit', action='store_true')
args = parser.parse_args()

if args.version:
    # Print version and exit
    import plyr
    print('Lyvi %s, using libglyr %s' % (VERSION, plyr.version().split()[1]))
    sys.exit()

# Read configuration file
config_file = args.config_file or os.environ['HOME'] + '/.config/lyvi/lyvi.conf'
if os.path.exists(config_file):
    config.update((k, v) for k, v in runpy.run_path(config_file).items() if k in config)
elif args.config_file:
    print('Configuration file not found: ' + config_file)
    sys.exit()

import inspect
import lyvi.players
if args.list_players:
    # Print a list of supported players and exit
    print('\033[1mSupported players:\033[0m')
    for name, obj in inspect.getmembers(lyvi.players):
        if inspect.ismodule(obj) and name != 'player':
            print('* ' + name)
    sys.exit()
player = None
if config['default_player'] and getattr(lyvi.players, config['default_player']).Player.running():
    # Use default player
    player = getattr(lyvi.players, config['default_player']).Player()
else:
    # Try to autodetect running player
    for name, obj in inspect.getmembers(lyvi.players):
        if inspect.ismodule(obj) and name != 'player' and obj.Player.running():
            player = obj.Player()
            break
if not player:
    print('No running supported player found!')
    sys.exit()
if args.command:
    player.send_command(args.command)
    sys.exit()

# Set up background
bg = None
if config['bg']:
    import lyvi.background
    if (config['bg_tmux_backdrops_pane'] is not None
            and config['bg_tmux_cover_pane'] is not None
            and config['bg_tmux_window_title'] is not None
            and 'TMUX' in os.environ):
        bg = lyvi.background.TmuxBackground()
    elif 'rxvt' in os.environ['TERM']:
        bg = lyvi.background.Background()

# Set up UI
import lyvi.tui
ui = lyvi.tui.Ui()

# Set up metadata
import lyvi.metadata
md = lyvi.metadata.Metadata()


def watch_player():
    while True:
        if not player.running():
            exit()
        player.get_status()
        if player.state == 'stop':
            md.reset_tags()
        elif (player.artist != md.artist
                or player.title != md.title
                or player.album != md.album):
            needsupdate = ['lyrics', 'guitartabs']
            if player.artist != md.artist:
                needsupdate += ['artistbio']
            if bg:
                if player.artist != md.artist:
                    needsupdate += ['backdrops']
                if player.album != md.album:
                    needsupdate += ['cover']
            md.set_tags()
            for item in needsupdate:
                thread(md.get, (item,))
        sleep(1)


def exit():
    ui.quit = True
    if bg:
        bg.cleanup()


def main():
    thread(watch_player)
    ui.init()
    try:
        ui.mainloop()
    except KeyboardInterrupt:
        exit()
