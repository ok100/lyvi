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
        return os.path.exists(os.path.join(os.environ['HOME'], '.moc', 'pid'))

    def get_info_value(self, info_line):
        """Extract 'A value' from line 'ValueName: A value'."""
        try:
            return info_line.split(maxsplit=1)[1]
        except IndexError:
            # Empty value.
            return None

    def get_status(self):
        data = {'artist': None, 'album': None, 'title': None, 'file': None, 'length': None}

        for line in check_output('mocp -i').splitlines():
            info_value = self.get_info_value(line)
            if line.startswith('State: '):
                data['state'] = info_value.lower()
            elif line.startswith('Artist: '):
                data['artist'] = info_value or ''
            elif line.startswith('Album: '):
                data['album'] = info_value or ''
            elif line.startswith('SongTitle: '):
                data['title'] = info_value or ''
            elif line.startswith('File: '):
                data['file'] = info_value
            elif line.startswith('TotalSec: '):
                data['length'] = int(info_value)

        for k in data:
            setattr(self, k, data[k])

    def send_command(self, command):
        cmd = {
            'play': 'mocp -U',
            'pause': 'mocp -P',
            'next': 'mocp -f',
            'prev': 'mocp -r',
            'stop': 'mocp -s',
            'volup': 'mocp --volume +5',
            'voldn': 'mocp --volume -5',
        }.get(command)

        if cmd:
            os.system(cmd)
            return True
