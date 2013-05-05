# Copyright (c) 2013 Ondrej Kipila <ok100 at lavabit dot com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os

import lyvi
from lyvi.utils import check_output, running


class Player:
    def __init__(self):
        # Get the path to music directory from MPD configuration file
        self.music_dir = None
        if os.path.exists(lyvi.config['mpd_config_file']):
            for line in open(lyvi.config['mpd_config_file']):
                if line.strip().startswith('music_directory'):
                    self.music_dir = line.split('"')[1]
                    if not self.music_dir.endswith('/'):
                        self.music_dir += '/'

    def get_status(self):
        if not running('mpd'):
            self.running = False
            return

        self.running = True

        status = check_output('mpc status')
        if '[playing]' in status:
            self.status = 'playing'
        elif '[paused]' in status:
            self.status = 'paused'
        else:
            self.status = 'stopped'
            self.artist = self.title = self.album = self.file = None
            return

        current = check_output('mpc current -f "%artist%\\%title%\\%album%\\%file%"')
        self.artist, self.title, self.album, self.file = current.split('\\')
