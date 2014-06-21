# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

"""Mpg123 plugin for Lyvi."""


import os

import lyvi
from lyvi.players import Player
from lyvi.utils import running


class Player(Player):
    LOG_FILE = os.path.join(lyvi.TEMP, 'mpg123.log')

    @classmethod
    def running(self):
        return running('mpg123') and os.path.exists(self.LOG_FILE)

    def get_status(self):
        data = {'artist': None, 'album': None, 'title': None, 'file': None, 'state': 'play', 'length': None}

        with open(self.LOG_FILE) as f:
            for line in f.read().splitlines():
                if 'Title:' and 'Artist:' in line:
                    data['title'], data['artist'] = (
                        x.strip() for x in line.split('Title: ')[1].split('Artist: ')
                    )
                elif 'Album: ' in line:
                    data['album'] = line.split('Album: ')[1].strip()

        for k in data:
            setattr(self, k, data[k])
