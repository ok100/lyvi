# Copyright (c) 2013 Ondrej Kipila <ok100 at lavabit dot com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

from threading import Lock
from time import sleep

import lyvi
import lyvi.glyr
from lyvi.utils import LoggingThread, cleanup


lock = Lock()


def get_and_update(view, artist, title):
    metadata = lyvi.glyr.get(view, artist, title)
    lock.acquire()
    try:
        if lyvi.ui.artist == artist and lyvi.ui.title == title:
            setattr(lyvi.ui, view, metadata)
            lyvi.ui.refresh()
    finally:
        lock.release()


def main():
    try:
        lyvi.ui.init()

        uiloop = LoggingThread(target=lyvi.ui.mainloop)
        uiloop.daemon = True
        uiloop.start()

        while True:
            lyvi.player.get_status()
            if not lyvi.player.running or lyvi.ui.quit:
                break

            if lyvi.player.status == 'stopped':
                lock.acquire()
                lyvi.ui.playing = False
                lyvi.ui.artist = lyvi.ui.title = None
                lyvi.ui.pos_y = 0
                lyvi.ui.refresh()
                lock.release()

            elif lyvi.player.artist != lyvi.ui.artist or lyvi.player.title != lyvi.ui.title:
                # New song
                lyvi.ui.playing = True

                needsupdate = ['lyrics', 'guitartabs']
                if lyvi.player.artist != lyvi.ui.artist:
                    needsupdate.append('artistbio')

                lock.acquire()
                if lyvi.ui.view in needsupdate:
                    lyvi.ui.pos_y = 0
                lyvi.ui.artist = lyvi.player.artist
                lyvi.ui.title = lyvi.player.title
                for view in needsupdate:
                    setattr(lyvi.ui, view, 'Searching %s...' %
                            ('guitar tabs' if view == 'guitartabs' else 'artist info' if view == 'artistbio' else view))
                lyvi.ui.refresh()
                lock.release()

                for view in needsupdate:
                    worker = LoggingThread(target=get_and_update,
                                           args=(view, lyvi.player.artist, lyvi.player.title))
                    worker.daemon = True
                    worker.start()

            sleep(1)

        cleanup()
    except:
        cleanup()
        if lyvi.args.debug:
            lyvi.logging.exception('Uncaught exception')
        raise
