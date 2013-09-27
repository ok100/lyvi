# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os

from lyvi.players import Player
from lyvi.utils import running, check_output


class Player(Player):
    @classmethod
    def running(self):
        return running('cmus')

    def get_status(self):
        data = {'artist': None, 'album': None, 'title': None, 'file': None}
        response = check_output('cmus-remote -Q')
        for line in response.splitlines():
            if line.startswith('status '):
                data['state'] = (line.split()[1].replace('playing', 'play')
                        .replace('paused', 'pause')
                        .replace('stopped', 'stop'))
            elif line.startswith('tag artist '):
                data['artist'] = line.split(' ', 2)[2]
            elif line.startswith('tag album '):
                data['album'] = line.split(' ', 2)[2]
            elif line.startswith('tag title '):
                data['title'] = line.split(' ', 2)[2]
            elif line.startswith('file '):
                data['file'] = line.split(' ', 1)[1]
        for k in data:
            setattr(self, k, data[k])

    def send_command(self, command):
        if command == 'play':
            os.system('cmus-remote -p')
        elif command == 'pause':
            os.system('cmus-remote -u')
        elif command == 'next':
            os.system('cmus-remote -n')
        elif command == 'prev':
            os.system('cmus-remote -r')
        elif command == 'stop':
            os.system('cmus-remote -s')
        elif command == 'volup':
            os.system('cmus-remote -v +5')
        elif command == 'voldn':
            os.system('cmus-remote -v -5')
