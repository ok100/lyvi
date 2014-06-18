# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

"""Shell-fm plugin for Lyvi."""


import os

from lyvi.players import Player
from lyvi.utils import process_socket, running


class Player(Player):
    NOWPLAYING_FILE = os.path.join(os.environ['HOME'], '.shell-fm', 'nowplaying')
    SOCKET = os.path.join(os.environ['HOME'], '.shell-fm', 'socket')

    @classmethod
    def running(self):
        return running('shell-fm') and os.path.exists(self.NOWPLAYING_FILE)

    def get_status(self):
        data = {'artist': None, 'album': None, 'title': None, 'file': None, 'state': 'stop'}

        with open(self.NOWPLAYING_FILE) as f:
            data['artist'], data['title'], data['album'], data['state'] = f.read().split('|')
        for x, y in (
            ('PLAYING', 'play'),
            ('PAUSED', 'pause'),
            ('STOPPED', 'stop')
        ):
            data['state'] = data['state'].replace(x, y)

        for k in data:
            setattr(self, k, data[k])

    def send_command(self, command):
        if not os.path.exists(self.SOCKET):
            return

        cmd = {
            'pause': 'pause',
            'next': 'skip',
            'stop': 'stop',
            'volup': 'volume +5',
            'voldn': 'volume -5',
        }.get(command)

        if cmd:
            process_socket(self.SOCKET, cmd)
            return True
