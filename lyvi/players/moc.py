# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

"""MOC plugin for Lyvi."""


import os

from lyvi.players import Player
from lyvi.utils import check_output


class Player(Player):
    @classmethod
    def running(self):
        return os.path.exists(os.environ['HOME'] + '/.moc/pid')

    def get_status(self):
        data = {'artist': None, 'album': None, 'title': None, 'file': None, 'length': None}

        for line in check_output('mocp -i 2> /dev/null').splitlines():
            if line.startswith('State: '):
                data['state'] = (line.split()[1]
                        .replace('PLAY', 'play')
                        .replace('PAUSE', 'pause')
                        .replace('STOP', 'stop'))
            elif line.startswith('Artist: '):
                data['artist'] = line.split(' ', 1)[1]
            elif line.startswith('Album: '):
                data['album'] = line.split(' ', 1)[1]
            elif line.startswith('SongTitle: '):
                data['title'] = line.split(' ', 1)[1]
            elif line.startswith('File: '):
                data['file'] = line.split(' ', 1)[1]
            elif line.startswith('TotalSec: '):
                data['length'] = int(line.split(' ', 1)[1])

        for k in data:
            setattr(self, k, data[k])

    def send_command(self, command):
        cmd = {
            'play': 'mocp -U 2> /dev/null',
            'pause': 'mocp -P 2> /dev/null',
            'next': 'mocp -f 2> /dev/null',
            'prev': 'mocp -r 2> /dev/null',
            'stop': 'mocp -s 2> /dev/null',
            'volup': 'mocp --volume +5 2> /dev/null',
            'voldn': 'mocp --volume -5 2> /dev/null',
        }.get(command)
        
        if cmd:
            os.system(cmd)
            return True
