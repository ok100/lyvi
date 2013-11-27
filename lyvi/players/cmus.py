# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

"""Cmus plugin for Lyvi."""


import os

from lyvi.players import Player
from lyvi.utils import check_output


class Player(Player):
    @classmethod
    def running(self):
        return os.system('cmus-remote -C') == 0

    def get_status(self):
        data = {'artist': None, 'album': None, 'title': None, 'file': None, 'length': None}

        for line in check_output('cmus-remote -Q').splitlines():
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
            elif line.startswith('duration '):
                data['length'] = int(line.split(' ', 1)[1])

        for k in data:
            setattr(self, k, data[k])

    def send_command(self, command):
        cmd = {
            'play': 'cmus-remote -p',
            'pause': 'cmus-remote -u',
            'next': 'cmus-remote -n',
            'prev': 'cmus-remote -r',
            'stop': 'cmus-remote -s',
            'volup': 'cmus-remote -v +5',
            'voldn': 'cmus-remote -v -5',
        }.get(command)

        if cmd:
            os.system(cmd)
            return True
