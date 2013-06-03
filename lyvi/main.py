# Copyright (c) 2013 Ondrej Kipila <ok100 at lavabit dot com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os
from threading import Thread
from time import sleep

import lyvi
import lyvi.metadata


def watch_player():
    while True:
        lyvi.player.get_status()
        if not lyvi.player.running:
            lyvi.ui.exit()

        if lyvi.player.status == 'stopped':
            lyvi.lock.acquire()
            lyvi.ui.artist = lyvi.ui.title = lyvi.ui.album = None
            lyvi.ui.update()
            lyvi.lock.release()
            if lyvi.bg:
                lyvi.bg.unset()

        elif lyvi.player.artist != lyvi.ui.artist \
                or lyvi.player.title != lyvi.ui.title \
                or lyvi.player.album != lyvi.ui.album:
            # New song
            needsupdate = ['lyrics', 'guitartabs']
            if lyvi.player.artist != lyvi.ui.artist:
                needsupdate.append('artistbio')

            if lyvi.ui.view in needsupdate:
                lyvi.ui.home()

            lyvi.lock.acquire()
            lyvi.ui.artist = lyvi.player.artist
            lyvi.ui.title = lyvi.player.title
            lyvi.ui.album = lyvi.player.album
            for view in needsupdate:
                setattr(lyvi.ui, view, 'Searching %s...' %
                    ('guitar tabs' if view == 'guitartabs'
                    else 'artist info' if view == 'artistbio' else view))
            lyvi.ui.update()
            lyvi.lock.release()

            for view in needsupdate:
                worker = Thread(target=lyvi.metadata.get_and_update,
                    args=(view, lyvi.player.artist, lyvi.player.title, lyvi.player.album))
                worker.daemon = True
                worker.start()

            if lyvi.bg and ((lyvi.bg.type == 'backdrops' and lyvi.player.artist != lyvi.bg.artist)
                    or (lyvi.bg.type == 'cover' and lyvi.player.album != lyvi.bg.album)):
                lyvi.bg.artist = lyvi.player.artist
                lyvi.bg.title = lyvi.player.title
                lyvi.bg.album = lyvi.player.album
                worker = Thread(target=lyvi.bg.update)
                worker.daemon = True
                worker.start()

        sleep(1)


def main():
    worker = Thread(target=watch_player)
    worker.daemon = True
    worker.start()

    lyvi.ui.init()
    lyvi.ui.loop.run()

    if lyvi.bg:
        lyvi.bg.unset()
        for file in os.listdir(lyvi.TEMP):
            if file.startswith('lyvi-%s' % lyvi.PID):
                os.remove('%s/%s' % (lyvi.TEMP, file))
