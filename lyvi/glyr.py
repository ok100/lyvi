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


def get(type, artist, title):
    query = plyr.Query(get_type=type, artist=artist, title=title)
    query.useragent = 'lyvi/%s' % lyvi.VERSION
    query.database = cache
    items = query.commit()

    if items:
        return items[0].data.decode()
    return None
