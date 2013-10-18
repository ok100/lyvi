# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

"""A package which contains all player-related code."""


import importlib
import sys

import lyvi


# List of all player-specific submodules
players = ['cmus', 'moc', 'mpg123', 'pianobar', 'shell-fm', 'mplayer', 'mpd', 'mpris']


def list():
    """Print a list of supported players."""
    print('\033[1mSupported players:\033[0m')
    for player in sorted(players):
        print('* ' + player)


def find():
    """Return the initialized player class, or None if no player was found."""
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
    """Base Player class.

    This class should be subclassed for a specific player.
    """

    def _getter(var):
        def get(self):
            return getattr(self, var)
        return get

    def _setter(var, vtype):
        def set(self, value):
            # Check if the property has the right type
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

    _state = 'stop'
    _artist = _album = _title = _file = _length = None
    artist = property(_getter('_artist'), _setter('_artist', str))
    album = property(_getter('_album'), _setter('_album', str))
    title = property(_getter('_title'), _setter('_title', str))
    file = property(_getter('_file'), _setter('_file', str))
    length = property(_getter('_length'), _setter('_length', int))
    state = property(_getter('_state'), _setter('_state', ('play', 'pause', 'stop')))
    
    @classmethod
    def running(self):
        """Return True if the player is running."""
        raise NotImplementedError('running() should be implemented in subclass') 

    def get_status(self):
        """Set the class properties to the actual values.

        Properties:
        state -- string
        artist -- string
        album -- string
        title -- string
        file -- string
        length -- int (in seconds)

        Property 'state' must be one of: 'play', 'pause', 'stop', other properties can be None.
        """
        raise NotImplementedError('get_status() should be implemented in subclass') 

    def send_command(self, command):
        """Send a given command to the player. Return True if the command was recognized.
        This method don't have to implement all commands.

        Keyword arguments:
        command -- a command to send
        
        Command names:
        play -- start playback
        pause -- pause playback
        next -- next song
        prev -- previous song
        stop -- stop playback
        volup -- volume up
        voldn -- volume down
        """
        pass


# Import all players from the players list
for player in players:
    importlib.import_module('lyvi.players.' + player)
