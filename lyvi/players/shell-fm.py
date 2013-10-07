# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os

from lyvi.players import Player
from lyvi.utils import process_socket, running


class Player(Player):
    NOWPLAYING_FILE = os.environ['HOME'] + '/.shell-fm/nowplaying'
    SOCKET = os.environ['HOME'] + '/.shell-fm/socket'

    @classmethod
    def running(self):
        return os.path.exists(self.SOCKET)

    def get_status(self):
        data = {'artist': None, 'album': None, 'title': None, 'file': None, 'state': 'stop'}
        if os.path.exists(self.NOWPLAYING_FILE):
            with open(self.NOWPLAYING_FILE) as f:
                data['artist'], data['title'], data['album'], data['state'] = f.read().split('|')
            data['state'] = (data['state']
                    .replace('PLAYING', 'play')
                    .replace('PAUSED', 'pause')
                    .replace('STOPPED', 'stop'))
        for k in data:
            setattr(self, k, data[k])

    def send_command(self, command):
        if command == 'pause':
            process_socket(self.SOCKET, 'pause')
        elif command == 'next':
            process_socket(self.SOCKET, 'skip')
        elif command == 'stop':
            process_socket(self.SOCKET, 'stop')
        elif command == 'volup':
            process_socket(self.SOCKET, 'volume +5')
        elif command == 'voldn':
            process_socket(self.SOCKET, 'volume -5')
