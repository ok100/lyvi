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
    config = {
        'act_songpausetoggle': 'p',
        'act_songnext': 'n',
        'act_volup': ')',
        'act_voldown': '(',
    }

    @classmethod
    def running(self):
        return running('pianobar') and os.path.exists(self.NOWPLAYING_FILE)

    def __init__(self):
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
        if not os.path.exists(self.FIFO)
            return

        cmd = {
            'play': 'act_songpausetoggle',
            'pause': 'act_songpausetoggle',
            'next': 'act_songnext',
            'volup': 'act_volup',
            'voldn': 'act_voldown',
        }.get(command)

        if cmd:
            process_fifo(self.FIFO, self.config[cmd])
            return True
