# Copyright (c) 2013 Ondrej Kipila <ok100 at lavabit dot com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os
from time import sleep

import lyvi
from lyvi.metadata import get_and_update
from lyvi.utils import thread


def watch_player():
    while True:
        lyvi.player.get_status()
        if not lyvi.player.running:
            lyvi.ui.exit()

        if lyvi.player.status == 'stopped':
            lyvi.ui.reset_tags()
            with lyvi.ui.lock:
                lyvi.ui.update()
            if lyvi.bg:
                lyvi.bg.reset_tags()
                with lyvi.bg.lock:
                    lyvi.bg.update()

        elif (lyvi.player.artist != lyvi.ui.artist
                or lyvi.player.title != lyvi.ui.title
                or lyvi.player.album != lyvi.ui.album):
            needsupdate = ['lyrics', 'guitartabs']
            if lyvi.player.artist != lyvi.ui.artist:
                needsupdate += ['artistbio']
            if lyvi.bg:
                if lyvi.player.artist != lyvi.bg.artist:
                    needsupdate += ['backdrops']
                if lyvi.player.album != lyvi.bg.album:
                    needsupdate += ['cover']
                lyvi.bg.set_tags()
            lyvi.ui.set_tags()
            for item in needsupdate:
                thread(get_and_update, (item,))
        sleep(1)


def main():
    thread(watch_player)

    lyvi.ui.init()

    try:
        lyvi.ui.loop.run()
    except KeyboardInterrupt:
        pass
    finally:
        if lyvi.bg:
            lyvi.bg.cleanup()
