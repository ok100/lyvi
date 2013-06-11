# Copyright (c) 2013 Ondrej Kipila <ok100 at lavabit dot com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os

import plyr

import lyvi


cache_dir = os.environ['HOME'] + '/.local/share/lyvi'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
cache = plyr.Database(cache_dir)


def cache_delete(type, artist, title, album):
    cache.delete(plyr.Query(get_type=type, artist=artist, title=title, album=album))


def get(type, artist, title, album):
    query = plyr.Query(get_type=type, artist=artist, title=title, album=album)
    query.useragent = lyvi.USERAGENT
    query.database = cache
    items = query.commit()
    if items:
        return items[0].data if type in ('backdrops', 'cover') else items[0].data.decode()
    return None


def get_and_update(type):
    artist = lyvi.ui.artist
    title = lyvi.ui.title
    album = lyvi.ui.album

    if type in ('lyrics', 'artistbio', 'guitartabs'):
        with lyvi.ui.lock:
            setattr(lyvi.ui, type, 'Searching %s...' %
                ('guitar tabs' if type == 'guitartabs'
                else 'artist info' if type == 'artistbio' else type))
            lyvi.ui.update()

    data = get(type, artist, title, album)

    if type in ('backdrops', 'cover'):
        with lyvi.bg.lock:
            setattr(lyvi.bg, type, data)
            lyvi.bg.update()
    else:
        with lyvi.ui.lock:
            if type == lyvi.ui.view:
                lyvi.ui.home()
            if lyvi.ui.artist == artist and lyvi.ui.title == title:
                setattr(lyvi.ui, type, get(type, artist, title, album))
                lyvi.ui.update()
