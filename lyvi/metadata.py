# Copyright (c) 2013 Ondrej Kipila <ok100 at lavabit dot com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import lyvi
import lyvi.glyr


def get_and_update(type, artist, title, album):
    metadata = lyvi.glyr.get(type, artist, title, album)
    lyvi.lock.acquire()
    try:
        if lyvi.ui.artist == artist and lyvi.ui.title == title:
            setattr(lyvi.ui, type, metadata)
            lyvi.ui.update()
    finally:
        lyvi.lock.release()
