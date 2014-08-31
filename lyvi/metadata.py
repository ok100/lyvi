# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

"""Metadata-related code."""


import os
import random
from threading import Lock

import plyr

import lyvi


class Metadata:
    """A class which holds metadata for the currently playing song."""
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

    @lyrics.setter
    def lyrics(self, value):
        """Update ui and save the lyrics."""
        self._lyrics = value
        lyvi.ui.update()
        if lyvi.ui.autoscroll:
            lyvi.ui.autoscroll.reset()
        if lyvi.config['save_lyrics']:
            self.save('lyrics', lyvi.config['save_lyrics'])

    @property
    def artistbio(self):
        return self._artistbio

    @artistbio.setter
    def artistbio(self, value):
        """Update UI."""
        self._artistbio = value
        lyvi.ui.update()

    @property
    def guitartabs(self):
        return self._guitartabs

    @guitartabs.setter
    def guitartabs(self, value):
        """Update UI."""
        self._guitartabs = value
        lyvi.ui.update()

    @property
    def backdrops(self):
        return self._backdrops

    @backdrops.setter
    def backdrops(self, value):
        """Update background."""
        self._backdrops = value
        if lyvi.bg:
            lyvi.bg.update()

    @property
    def cover(self):
        return self._cover

    @cover.setter
    def cover(self, value):
        """Update background and save the cover."""
        self._cover = value
        if lyvi.bg:
            lyvi.bg.update()
        if lyvi.config['save_cover']:
            self.save('cover', lyvi.config['save_cover_filename'])

    def __init__(self):
        """Initialize the class."""
        cache_dir = os.path.join(os.environ['HOME'], '.local/share/lyvi')
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        self.cache = plyr.Database(cache_dir)
        self.lock = Lock()

    def set_tags(self):
        """Set all tag properties to the actual values."""
        self.artist = lyvi.player.artist
        self.title = lyvi.player.title
        self.album = lyvi.player.album
        self.file = lyvi.player.file

    def reset_tags(self):
        """Set all tag and metadata properties to None."""
        self.artist = self.title = self.album = self.file = None
        self.lyrics = self.artistbio = self.guitartabs = None
        self.backdrops = self.cover = None

    def delete(self, type, artist, title, album):
        """Delete metadata from the cache.

        Keyword arguments:
        type -- type of the metadata
        artist -- artist tag
        title -- title tag
        album -- album tag
        """
        if artist and title and album:
            self.cache.delete(plyr.Query(get_type=type, artist=artist, title=title, album=album))

    def save(self, type, file):
        """Save the given metadata type.

        Keyword arguments:
        type -- type of the metadata
        file -- path to the file metadata will be saved to

        Some special substrings can be used in the filename:
        <filename> -- name of the current song without extension
        <songdir> -- directory containing the current song
        <artist> -- artist of the current song
        <title> -- title of the current song
        <album> -- album of the current song
        """
        data = getattr(self, type)
        if self.file and data and data != 'Searching...':
            for k, v in {
                '<filename>': os.path.splitext(os.path.basename(self.file))[0],
                '<songdir>': os.path.dirname(self.file),
                '<artist>': self.artist,
                '<title>': self.title,
                '<album>': self.album
            }.items():
                file = file.replace(k, v)
            if not os.path.exists(os.path.dirname(file)):
                os.makedirs(os.path.dirname(file))
            if not os.path.exists(file):
                mode = 'wb' if isinstance(data, bytes) else 'w'
                with open(file, mode) as f:
                    f.write(data)

    def _query(self, type, normalize=True, number=1):
        """Return a list containing results from glyr.Query,
        or None if some tags are missing.

        Keyword arguments:
        type -- type of the metadata
        normalize -- whether the search strings should be normalized by glyr
        """
        try:
            query = plyr.Query(
                number=number,
                parallel=20,
                get_type=type,
                artist=self.artist,
                title=self.title,
                album=self.album
            )
        except AttributeError:  # Missing tags?
            return None
        query.useragent = lyvi.USERAGENT
        query.database = self.cache
        if not normalize:
            query.normalize = ('none', 'artist', 'album', 'title')
        return query.commit()

    def get(self, type):
        """Download and set the metadata for the given property.

        Keyword arguments:
        type -- type of the metadata
        """
        if lyvi.ui.view == type:
            lyvi.ui.home()

        artist = self.artist
        title = self.title

        number = 1
        if type in ('lyrics', 'artistbio', 'guitartabs'):
            setattr(self, type, 'Searching...')
        elif type in ('backdrops', 'cover'):
            setattr(self, type, None)
            if type == 'backdrops':
                number = 20

        items = (self._query(type, number=number)
                 or self._query(type, number=number, normalize=False))
        data = None
        if items:
            if type == 'backdrops':
                data = random.choice(items).data
            elif type == 'cover':
                data = items[0].data
            else:
                data = items[0].data.decode()
        with self.lock:
            if artist == self.artist and title == self.title:
                setattr(self, type, data)
