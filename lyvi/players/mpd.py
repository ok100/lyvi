# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os
import telnetlib

import lyvi
from lyvi.players import Player
from lyvi.utils import running


class Player(Player):
    @classmethod
    def running(self):
        return (lyvi.config['mpd_host'] not in ('localhost', '127.0.0.1') or running('mpd'))

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
        cmd = {
            'play': b'play\n',
            'pause': b'pause\n',
            'next': b'next\n',
            'prev': b'previous\n',
            'stop': b'stop\n',
        }.get(command)

        if cmd:
            self.telnet.write(cmd)
            return True
    
    def __del__(self):
        self.telnet.close()
