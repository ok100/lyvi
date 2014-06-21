# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

"""Xmms2 plugin for Lyvi."""


import os
from urllib.parse import unquote_plus

from lyvi.players import Player
from lyvi.utils import running, check_output


class Player(Player):
    @classmethod
    def running(self):
        return running('xmms2d')

    def get_status(self):
        data = {'artist': None, 'album': None, 'title': None, 'file': None, 'state': 'play', 'length': None}
        try:
            data['state'], data['artist'], data['album'], data['title'], data['file'], data['length'] = \
                check_output('xmms2 current -f \'${playback_status}|${artist}|${album}|${title}|${url}|${duration}\'').split('|')
        except ValueError:
            return

        for x, y in (('Playing', 'play'), ('Paused', 'pause'), ('Stopped', 'stop')):
            data['state'] = data['state'].replace(x, y)

        # unquote_plus replaces % not as plus signs but as spaces (url decode)
        data['file'] = unquote_plus(data['file']).strip()
        for x, y in (('\'', ''), ('file://', '')):
            data['file'] = data['file'].replace(x, y)

        try:
            data['length'] = int(data['length'].split(':')[0]) * 60 + int(data['length'].split(':')[1])
        except ValueError:
            data['length'] = None

        for k in data:
            setattr(self, k, data[k])

    def send_command(self, command):
        cmd = {
            'play': 'xmms2 play',
            'pause': 'xmms2 pause',
            'next': 'xmms2 jump +1',
            'prev': 'xmms2 jump -1',
            'stop': 'xmms2 stop',
            'volup': 'xmms2 server volume +5',
            'voldn': 'xmms2 server volume -5',
        }.get(command)

        if cmd:
            os.system(cmd)
            return True
