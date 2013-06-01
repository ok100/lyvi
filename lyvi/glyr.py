# Copyright (c) 2013 Ondrej Kipila <ok100 at lavabit dot com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os

import plyr

import lyvi


cache_dir = '%s/.local/share/lyvi' % os.environ['HOME']
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
cache = plyr.Database(cache_dir)


def cache_delete(type, artist, title, album):
    cache.delete(plyr.Query(get_type=type, artist=artist, title=title, album=album))


def get(type, artist, title, album):
    query = plyr.Query(get_type=type, artist=artist, title=title, album=album)
    query.useragent = 'lyvi/%s' % lyvi.VERSION
    query.database = cache
    items = query.commit()

    return items[0].data.decode() if items else None


def get_and_update(type, artist, title, album):
    metadata = get(type, artist, title, album)
    lyvi.lock.acquire()
    try:
        if lyvi.ui.artist == artist and lyvi.ui.title == title:
            setattr(lyvi.ui, type, metadata)
            lyvi.ui.update()
    finally:
        lyvi.lock.release()
