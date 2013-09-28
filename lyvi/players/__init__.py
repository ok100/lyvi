# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import importlib
import sys

import lyvi


players = ['cmus', 'moc', 'mpd', 'mpris']


def list():
    print('\033[1mSupported players:\033[0m')
    for player in sorted(players):
        print('* ' + player)


def find():
    players.pop(players.index('mpris'))
    if lyvi.config['default_player']:
        if mpris.running(lyvi.config['default_player']):
            return mpris.Player(lyvi.config['default_player'])
        players.insert(0, players.pop(players.index(lyvi.config['default_player'])))
    obj = mpris.find()
    if obj:
        return obj
    for name in players:
        obj = getattr(sys.modules[__name__], name).Player
        if obj.running():
            return obj()
    return None


class Player:
    _state = 'stop'
    artist = None
    album = None
    title = None
    file = None
    
    @property
    def state(self):
        return self._state
    @state.setter
    def state(self, value):
        if value in ('play', 'pause', 'stop'):
            self._state = value
        else:
            raise ValueError('incorrect state value')

    @classmethod
    def running(self):
        raise NotImplementedError('found() should be implemented in subclass') 

    def get_status(self):
        raise NotImplementedError('get_status() should be implemented in subclass') 

    def send_command(self, command):
        raise NotImplementedError('send_command() should be implemented in subclass') 


for player in players:
    importlib.import_module('lyvi.players.' + player)
