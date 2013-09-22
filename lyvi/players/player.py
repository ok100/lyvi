# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

class _Player:
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
