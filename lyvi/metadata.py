# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os
from threading import Lock

import plyr

import lyvi


class Metadata:
    artist = None
    album = None
    title = None
    file = None
    _lyrics = None
    _artistbio = None
    _guitartabs = None
    _backdrops = None
    _cover = None

    @property
    def lyrics(self):
        return self._lyrics

    @property
    def artistbio(self):
        return self._artistbio

    @property
    def guitartabs(self):
        return self._guitartabs

    @property
    def backdrops(self):
        return self._backdrops

    @property
    def cover(self):
        return self._cover

    @lyrics.setter
    def lyrics(self, value):
        self._lyrics = value
        lyvi.ui.update()
        if lyvi.ui.autoscroll:
            lyvi.ui.autoscroll.reset()
        if lyvi.config['save_lyrics']:
            self.save('lyrics', lyvi.config['save_lyrics_filename'])

    @artistbio.setter
    def artistbio(self, value):
        self._artistbio = value
        lyvi.ui.update()

    @guitartabs.setter
    def guitartabs(self, value):
        self._guitartabs = value
        lyvi.ui.update()

    @backdrops.setter
    def backdrops(self, value):
        self._backdrops = value
        if lyvi.bg:
            lyvi.bg.update()

    @cover.setter
    def cover(self, value):
        self._cover = value
        if lyvi.bg:
            lyvi.bg.update()
        if lyvi.config['save_cover']:
            self.save('cover', lyvi.config['save_cover_filename'])

    def __init__(self):
        cache_dir = os.environ['HOME'] + '/.local/share/lyvi'
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        self.cache = plyr.Database(cache_dir)
        self.lock = Lock()

    def set_tags(self):
        self.artist = lyvi.player.artist
        self.title = lyvi.player.title
        self.album = lyvi.player.album
        self.file = lyvi.player.file

    def reset_tags(self):
        self.artist = self.title = self.album = self.file = None
        self.lyrics = self.artistbio = self.guitartabs = None
        self.backdrops = self.cover = None

    def delete(self, type, artist, title, album):
        if artist and title and album:
            self.cache.delete(plyr.Query(get_type=type, artist=artist, title=title, album=album))

    def save(self, type, filename):
        data = getattr(self, type)
        if self.file and data and data != 'Searching...':
            replace = {
                '<filename>': self.file.rsplit('/', 1)[1].rsplit('.', 1)[0],
                '<songdir>': self.file.rsplit('/', 1)[0],
                '<artist>': self.artist,
                '<title>': self.title,
                '<album>': self.album
            }
            file = filename
            for k in replace:
                file = file.replace(k, replace[k])
            if not os.path.exists(file.rsplit('/', 1)[0]):
                os.makedirs(file.rsplit('/', 1)[0])
            if not os.path.exists(file):
                mode = 'wb' if isinstance(data, bytes) else 'w'
                with open(file, mode) as f:
                    f.write(data)

    def _query(self, type, normalize=True):
        try:
            query = plyr.Query(get_type=type, artist=self.artist, title=self.title, album=self.album)
        except AttributeError:
            # Missing tags?
            return None
        else:
            query.useragent = lyvi.USERAGENT
            query.database = self.cache
            if not normalize:
                query.normalize = ('none', 'artist', 'album', 'title')
            return query.commit()

    def get(self, type):
        artist = self.artist
        title = self.title
        if lyvi.ui.view == type:
            lyvi.ui.home()
        if type in ('lyrics', 'artistbio', 'guitartabs'):
            setattr(self, type, 'Searching...')
        items = self._query(type, normalize=False) or self._query(type)
        data = None
        if items:
            if type in ('backdrops', 'cover'):
                data = items[0].data
            else:
                data = items[0].data.decode()
        with self.lock:
            if artist == self.artist and title == self.title:
                setattr(self, type, data)
