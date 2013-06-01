# Copyright (c) 2013 Ondrej Kipila <ok100 at lavabit dot com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

from threading import Thread
from time import sleep

import lyvi
import lyvi.glyr


def watch_player():
    while True:
        lyvi.player.get_status()
        if not lyvi.player.running:
            lyvi.ui.exit()

        if lyvi.player.status == 'stopped':
            lyvi.lock.acquire()
            lyvi.ui.artist = lyvi.ui.title = None
            lyvi.ui.update()
            lyvi.lock.release()

        elif lyvi.player.artist != lyvi.ui.artist \
                or lyvi.player.title != lyvi.ui.title:
            # New song
            needsupdate = ['lyrics', 'guitartabs']
            if lyvi.player.artist != lyvi.ui.artist:
                needsupdate.append('artistbio')
            if lyvi.ui.view in needsupdate:
                lyvi.ui.home()
            lyvi.lock.acquire()
            lyvi.ui.artist = lyvi.player.artist
            lyvi.ui.title = lyvi.player.title
            for view in needsupdate:
                setattr(lyvi.ui, view, 'Searching %s...' %
                    ('guitar tabs' if view == 'guitartabs'
                    else 'artist info' if view == 'artistbio' else view))
            lyvi.ui.update()
            lyvi.lock.release()
            for view in needsupdate:
                worker = Thread(target=lyvi.glyr.get_and_update,
                    args=(view, lyvi.player.artist, lyvi.player.title))
                worker.daemon = True
                worker.start()

        sleep(1)


def main():
    worker = Thread(target=watch_player)
    worker.daemon = True
    worker.start()

    lyvi.ui.init()
    lyvi.ui.loop.run()
