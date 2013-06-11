# Copyright (c) 2013 Ondrej Kipila <ok100 at lavabit dot com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os
import telnetlib

import lyvi


# Get the path to music directory from MPD configuration file
music_dir = None
if os.path.exists(lyvi.config['mpd_config_file']):
    for line in open(lyvi.config['mpd_config_file']):
        if line.strip().startswith('music_directory'):
            music_dir = line.split('"')[1]
            if not music_dir.endswith('/'):
                music_dir += '/'


class Player:
    def __init__(self):
        self.running = True
        self.status = 'stop'
        self.telnet = telnetlib.Telnet(lyvi.config['mpd_host'], lyvi.config['mpd_port'])
        self.telnet.read_until(b'\n')

    def get_status(self):
        self.artist = self.album = self.title = self.file = None
        self.telnet.write(b'status\n')
        response = self.telnet.read_until(b'OK').decode()
        self.telnet.write(b'currentsong\n')
        response += self.telnet.read_until(b'OK').decode()
        data = {
            'state: ': 'status',
            'Artist: ': 'artist',
            'Title: ': 'title',
            'Album: ': 'album',
            'file: ': 'title',
        }
        for line in response.splitlines():
            for k in data:
                if line.startswith(k):
                    setattr(self, data[k], line.split(k, 1)[1])
                    break
        self.file = music_dir + self.file if self.file and music_dir else None
    
    def __del__(self):
        self.telnet.close()
