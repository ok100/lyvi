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


def parse_args():
    parser = argparse.ArgumentParser(prog='lyvi')
    parser.add_argument('command', nargs='?',
        help='send a command to the player and exit')
    parser.add_argument('-c', '--config-file',
        help='path to an alternate config file')
    parser.add_argument('-l', '--list-players',
        help='print a list of supported players and exit', action='store_true')
    parser.add_argument('-v', '--version',
        help='print version information and exit', action='store_true')
    return parser.parse_args()


def parse_config():
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
    file = args.config_file or os.environ['HOME'] + '/.config/lyvi/lyvi.conf'
    if os.path.exists(file):
        config.update((k, v) for k, v in runpy.run_path(file).items() if k in config)
        return config
    elif args.config_file:
        print('Configuration file not found: ' + file)
        sys.exit()


def print_version():
    import plyr
    print('Lyvi %s, using libglyr %s' % (VERSION, plyr.version().split()[1]))


def init_background():
    if config['bg']:
        import lyvi.background
        if (config['bg_tmux_backdrops_pane'] is not None
                and config['bg_tmux_cover_pane'] is not None
                and config['bg_tmux_window_title'] is not None
                and 'TMUX' in os.environ):
            return lyvi.background.TmuxBackground()
        elif 'rxvt' in os.environ['TERM']:
            return lyvi.background.Background()
    return None


def init_ui():
    import lyvi.tui
    return lyvi.tui.Ui()


def init_metadata():
    import lyvi.metadata
    return lyvi.metadata.Metadata()


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


args = parse_args()
config = parse_config()
if args.version:
    print_version()
    sys.exit()
import lyvi.players
if args.list_players:
    lyvi.players.list()
    sys.exit()
player = lyvi.players.find()
if args.command:
    player.send_command(args.command)
    sys.exit()
bg = init_background()
md = init_metadata()
ui = init_ui()
