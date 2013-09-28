# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os

from lyvi.players import Player
from lyvi.utils import check_output


class Player(Player):
    @classmethod
    def running(self):
        return os.path.exists(os.environ['HOME'] + '/.moc/pid')

    def get_status(self):
        data = {'artist': None, 'album': None, 'title': None, 'file': None}
        response = check_output('mocp -i 2> /dev/null')
        for line in response.splitlines():
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
        for k in data:
            setattr(self, k, data[k])

    def send_command(self, command):
        if command == 'play':
            os.system('mocp -U 2> /dev/null')
        elif command == 'pause':
            os.system('mocp -P 2> /dev/null')
        elif command == 'next':
            os.system('mocp -f 2> /dev/null')
        elif command == 'prev':
            os.system('mocp -r 2> /dev/null')
        elif command == 'stop':
            os.system('mocp -s 2> /dev/null')
        elif command == 'volup':
            os.system('mocp --volume +5 2> /dev/null')
        elif command == 'voldn':
            os.system('mocp --volume -5 2> /dev/null')
