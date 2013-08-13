# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os
import telnetlib

import lyvi
from lyvi.players.player import _Player
from lyvi.utils import running


class Player(_Player):
    def found():
        if lyvi.config['mpd_host'] not in ('localhost', '127.0.0.1') or running('mpd'):
            return True
        return False

    def __init__(self):
        self.music_dir = None
        if os.path.exists(lyvi.config['mpd_config_file']):
            for line in open(lyvi.config['mpd_config_file']):
                if line.strip().startswith('music_directory'):
                    self.music_dir = line.split('"')[1]
                    if not self.music_dir.endswith('/'):
                        self.music_dir += '/'
        self.telnet = telnetlib.Telnet(lyvi.config['mpd_host'], lyvi.config['mpd_port'])
        self.telnet.read_until(b'\n')

    def get_status(self):
        tags = {'artist': None, 'album': None, 'title': None, 'file': None}
        self.telnet.write(b'status\n')
        response = self.telnet.read_until(b'OK').decode()
        self.telnet.write(b'currentsong\n')
        response += self.telnet.read_until(b'OK').decode()
        data = {
            'state: ': 'state',
            'Artist: ': 'artist',
            'Title: ': 'title',
            'Album: ': 'album',
            'file: ': 'file',
        }
        for line in response.splitlines():
            for k in data:
                if line.startswith(k):
                    tags[data[k]] = line.split(k, 1)[1]
                    break
        tags['file'] = self.music_dir + tags['file'] if tags['file'] and self.music_dir else None
        for k in tags:
            setattr(self, k, tags[k])

    def send_command(self, command):
        if command == 'play':
            self.telnet.write(b'play\n')
        elif command == 'pause':
            self.telnet.write(b'pause\n')
        elif command == 'next':
            self.telnet.write(b'next\n')
        elif command == 'prev':
            self.telnet.write(b'previous\n')
        elif command == 'stop':
            self.telnet.write(b'stop\n')
    
    def __del__(self):
        self.telnet.close()
