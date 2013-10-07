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

import lyvi.config_defaults
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
    config = dict(lyvi.config_defaults.defaults)
    file = args.config_file or os.environ['HOME'] + '/.config/lyvi/lyvi.conf'
    if os.path.exists(file):
        config.update((k, v) for k, v in runpy.run_path(file).items() if k in config)
    elif args.config_file:
        print('Configuration file not found: ' + file)
        sys.exit()
    return config


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
        pass
    finally:
        exit()


# Objects used across the whole package
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
if not player:
    print('No running supported player found!')
    sys.exit()
if args.command:
    player.send_command(args.command)
    sys.exit()
md = init_metadata()
bg = init_background()
ui = init_ui()
