# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

"""Command-line lyrics (and more!) viewer."""


import argparse
import os
import runpy
import signal
import sys
import time
from tempfile import gettempdir

import lyvi.config_defaults
from lyvi.utils import thread

# Make this PEP 386 compatible:
__version__ = '2.0-git'


USERAGENT = 'lyvi/' + __version__
TEMP = gettempdir()
PID = os.getpid()


def parse_args():
    """Return the populated Namespace of command-line args."""
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
    """Return a dict with updated configuration options."""
    config = dict(lyvi.config_defaults.defaults)
    file = args.config_file or os.path.join(os.environ['HOME'], '.config/lyvi/lyvi.conf')
    if os.path.exists(file):
        try:
            config.update((k, v) for k, v in runpy.run_path(file).items() if k in config)
        except:
            # Error in configuration file
            import traceback
            tbtype, tbvalue, tb = sys.exc_info()
            sys.stderr.write('\033[31mError in configuration file.\033[0m\n\n%s\n'
                    % ''.join(traceback.format_exception_only(tbtype, tbvalue)).strip())
            sys.exit(1)
    elif args.config_file:
        sys.stderr.write('Configuration file not found: ' + file + '\n')
        sys.exit(1)
    return config


def print_version():
    """Print version information."""
    import plyr
    print('Lyvi %s, using libglyr %s' % (__version__, plyr.version().split()[1]))


def init_background():
    """If background is enabled, return the initialized Background class,
    otherwise return None.
    """
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
    """Return the initialized Ui class."""
    import lyvi.tui
    return lyvi.tui.Ui()


def init_metadata():
    """Return the initialized Metadata class."""
    import lyvi.metadata
    return lyvi.metadata.Metadata()


def watch_player():
    """Main loop which checks for new song and updates the metadata."""
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
        time.sleep(1)


def exit(signum=None, frame=None):
    """Do the cleanup and exit the app.

    Parameters are not used, but required for signal callback.
    """
    ui.quit = True
    if bg:
        bg.cleanup()
    player.cleanup()


def main():
    """Start the app."""
    thread(watch_player)
    ui.init()
    try:
        ui.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
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
if not player:
    sys.stderr.write('No running supported player found!\n')
    sys.exit(1)
if args.command:
    if not player.send_command(args.command):
        sys.stderr.write('Unknown command: ' + args.command + '\n')
        sys.exit(1)
    sys.exit()
md = init_metadata()
bg = init_background()
ui = init_ui()

# Also do the cleanup when the terminal is closed
signal.signal(signal.SIGHUP, exit)
