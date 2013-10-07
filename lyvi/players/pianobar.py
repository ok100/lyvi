# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os

from lyvi.players import Player
from lyvi.utils import process_fifo, running


class Player(Player):
    NOWPLAYING_FILE = os.environ['HOME'] + '/.config/pianobar/nowplaying'
    FIFO = os.environ['HOME'] + '/.config/pianobar/ctl'

    @classmethod
    def running(self):
        return running('pianobar') and os.path.exists(self.NOWPLAYING_FILE)

    def __init__(self):
        self.config = {
            'act_songpausetoggle': 'p',
            'act_songnext': 'n',
            'act_volup': ')',
            'act_voldown': '(',
        }
        with open(os.environ['HOME'] + '/.config/pianobar/config') as f:
            for line in f.read().splitlines():
                if not line.strip().startswith('#') and line.split('=')[0].strip() in self.config:
                    self.config[line.split('=')[0].strip()] = line.split('=')[1].strip()

    def get_status(self):
        data = {'artist': None, 'album': None, 'title': None, 'file': None, 'state': 'play'}
        with open(self.NOWPLAYING_FILE) as f:
            data['artist'], data['title'], data['album'] = f.read().split('|')
        for k in data:
            setattr(self, k, data[k])

    def send_command(self, command):
        if command == 'play' or command == 'pause':
            process_fifo(self.FIFO, self.config['act_songpausetoggle'])
        elif command == 'next':
            process_fifo(self.FIFO, self.config['act_songnext'])
        elif command == 'volup':
            process_fifo(self.FIFO, self.config['act_volup'])
        elif command == 'voldn':
            process_fifo(self.FIFO, self.config['act_voldown'])
