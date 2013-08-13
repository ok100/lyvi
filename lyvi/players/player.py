# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

class _Player:
    _running = True
    _state = 'stop'
    artist = None
    album = None
    title = None
    file = None
    
    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value):
        if value is True or value is False:
            self._running = value
        else:
            raise ValueError('incorrect running value')

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if value in ('play', 'pause', 'stop'):
            self._state = value
        else:
            raise ValueError('incorrect state value')

    @staticmethod
    def found():
        raise NotImplementedError('found() should be implemented in subclass') 

    def get_status(self):
        raise NotImplementedError('get_status() should be implemented in subclass') 

    def send_command(self, command):
        raise NotImplementedError('send_command() should be implemented in subclass') 
