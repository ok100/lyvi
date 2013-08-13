# Copyright (c) 2013 Ondrej Kipila <ok100 at lavabit dot com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os
from time import sleep

import lyvi
from lyvi.utils import thread


def watch_player():
    while True:
        lyvi.player.get_status()
        if not lyvi.player.running:
            lyvi.ui.exit()
        if lyvi.player.state == 'stop':
            lyvi.md.reset_tags()
        elif (lyvi.player.artist != lyvi.md.artist
                or lyvi.player.title != lyvi.md.title
                or lyvi.player.album != lyvi.md.album):
            needsupdate = ['lyrics', 'guitartabs']
            if lyvi.player.artist != lyvi.md.artist:
                needsupdate += ['artistbio']
            if lyvi.bg:
                if lyvi.player.artist != lyvi.md.artist:
                    needsupdate += ['backdrops']
                if lyvi.player.album != lyvi.md.album:
                    needsupdate += ['cover']
            lyvi.md.set_tags()
            for item in needsupdate:
                thread(lyvi.md.get, (item,))
        sleep(1)


def main():
    thread(watch_player)
    lyvi.ui.init()
    try:
        lyvi.ui.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        if lyvi.bg:
            lyvi.bg.cleanup()
