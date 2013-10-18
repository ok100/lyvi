# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os

import lyvi
from lyvi.players import Player
from lyvi.utils import process_fifo, running

if not lyvi.config['mplayer_config_dir'].endswith('/'):
    lyvi.config['mplayer_config_dir'] = lyvi.config['mplayer_config_dir'] + '/'

class Player(Player):
    LOG_FILE = lyvi.config['mplayer_config_dir'] + 'log'
    FIFO = lyvi.config['mplayer_config_dir'] + 'fifo'
    ID = {
        'ID_CLIP_INFO_VALUE0=': 'title',
        'ID_CLIP_INFO_VALUE1=': 'artist',
        'ID_CLIP_INFO_VALUE3=': 'album',
        'ID_FILENAME=': 'file',
        'ID_LENGTH=': 'length',
    }

    @classmethod
    def running(self):
        return (running('mplayer') or running('mpv')) and os.path.exists(self.LOG_FILE)

    def get_status(self):
        data = {'artist': None, 'album': None, 'title': None, 'file': None, 'state': 'play', 'length': None}

        with open(self.LOG_FILE) as f:
            for line in f.read().splitlines():
                for i in self.ID:
                    if i in line:
                        data[self.ID[i]] = line.split(i)[1]

        if data['length']:
            data['length'] = int(data['length'].split('.')[0])

        for k in data:
            setattr(self, k, data[k])

    def send_command(self, command):
        if not os.path.exists(self.FIFO):
            return

        cmd = {
            'play': 'pause',
            'pause': 'pause',
            'next': 'pt_step 1',
            'prev': 'pt_step -1',
            'stop': 'stop',
            'volup': 'volume +5',
            'voldn': 'volume -5',
        }.get(command)

        if cmd:
            process_fifo(self.FIFO, cmd)
            return True
