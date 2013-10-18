# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import importlib
import sys

import lyvi


players = ['cmus', 'moc', 'mpg123', 'pianobar', 'shell-fm', 'mplayer', 'mpd', 'mpris']


def list():
    """Prints a list of supported players"""
    print('\033[1mSupported players:\033[0m')
    for player in sorted(players):
        print('* ' + player)


def find():
    """Returns the initialized player class, or None if no player was found"""
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
    _artist = None
    _album = None
    _title = None
    _file = None
    _length = None
    _state = 'stop'

    def _getter(var):
        def get(self):
            return getattr(self, var)
        return get

    def _setter(var, vtype):
        def set(self, value):
            if type(vtype) is tuple:
                if value in vtype:
                    setattr(self, var, value)
                else:
                    raise ValueError('unsupported value for \'%s\': %s' % (var[1:], value))
            elif isinstance(value, vtype) or value is None:
                setattr(self, var, value)
            else:
                raise ValueError('unsupported type for \'%s\': %s' % (var[1:], type(value).__name__))
        return set

    artist = property(_getter('_artist'), _setter('_artist', str))
    album = property(_getter('_album'), _setter('_album', str))
    title = property(_getter('_title'), _setter('_title', str))
    file = property(_getter('_file'), _setter('_file', str))
    length = property(_getter('_length'), _setter('_length', int))
    state = property(_getter('_state'), _setter('_state', ('play', 'pause', 'stop')))
    
    @classmethod
    def running(self):
        raise NotImplementedError('running() should be implemented in subclass') 

    def get_status(self):
        raise NotImplementedError('get_status() should be implemented in subclass') 

    def send_command(self, command):
        return


for player in players:
    importlib.import_module('lyvi.players.' + player)
