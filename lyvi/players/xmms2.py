# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

"""Xmms2 plugin for Lyvi."""


import os

import urllib.parse

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
                    check_output('xmms2 current -f \'${playback_status}|${artist}|${album}|${title}|${url}|${duration}\' 2> /dev/null').split('|')
        except ValueError:
            return

        data['state'] = (data['state']
                .replace('Playing', 'play')
                .replace('Paused', 'pause')
                .replace('Stopped', 'stop'))

        # unquote_plus replaces % not as plus signs but as spaces (url decode)
        data['file'] = (urllib.parse.unquote_plus(data['file']).strip()
                .replace('\'', '')
                .replace("file://", ""))

        try:
            data['length'] = int(data['length'].split(':')[0]) * 60 + int(data['length'].split(':')[1])
        except ValueError:
            data['length'] = None

        for k in data:
            setattr(self, k, data[k])

    def send_command(self, command):
        cmd = {
            'play': 'xmms2 play 2> /dev/null',
            'pause': 'xmms2 pause 2> /dev/null',
            'next': 'xmms2 jump +1 2> /dev/null',
            'prev': 'xmms2 jump -1 2> /dev/null',
            'stop': 'xmms2 stop 2> /dev/null',
            'volup': 'xmms2 server volume +5 2> /dev/null',
            'voldn': 'xmms2 server volume -5 2> /dev/null',
        }.get(command)

        if cmd:
            os.system(cmd)
            return True
