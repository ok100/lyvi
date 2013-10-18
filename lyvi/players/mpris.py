# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

"""MPRIS plugin for Lyvi."""


import dbus
import dbus.exceptions
import dbus.glib
import dbus.mainloop.glib
from gi.repository import GObject

from lyvi.players import Player
from lyvi.utils import thread


# Initialize the DBus loop, required to enable asynchronous dbus calls
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
GObject.threads_init()
dbus.glib.init_threads()
loop = GObject.MainLoop()
thread(loop.run)


def find():
    """Return the initialized mpris.Player class, otherwise
    return None if no player was found."""
    try:
        for name in dbus.SessionBus().list_names():
            if name.startswith('org.mpris.MediaPlayer2.'):
                return Player(name[len('org.mpris.MediaPlayer2.'):])
    except dbus.exceptions.DBusException:
        pass
    return None


def running(playername):
    """Return True if a MPRIS player with the given name is running.
    
    Keyword arguments:
    playername -- mpris player name
    """
    try:
        bus = dbus.SessionBus()
        bus.get_object('org.mpris.MediaPlayer2.%s' % playername, '/org/mpris/MediaPlayer2')
        return True
    except dbus.exceptions.DBusException:
        return False


class Player(Player):
    """Class which supports all players that implement the MPRIS Interface."""
    def running(self):
        return running(self.playername)

    def __init__(self, playername):
        """Initialize the player.

        Keyword arguments:
        playername -- mpris player name
        """
        self.playername = playername

        # Player status cache
        self.playerstatus = {}

        # Store the interface in this object, so it does not have to reinitialized each second
        # in the main loop
        bus = dbus.SessionBus()
        playerobject = bus.get_object('org.mpris.MediaPlayer2.' + self.playername,
                '/org/mpris/MediaPlayer2')
        self.mprisplayer = dbus.Interface(playerobject, 'org.mpris.MediaPlayer2.Player')
        self.mprisprops = dbus.Interface(playerobject, 'org.freedesktop.DBus.Properties')
        self.mprisprops.connect_to_signal("PropertiesChanged", self.loaddata)
        self.loaddata()

    def loaddata(self, *args, **kwargs):
        """Retrieve the player status over DBUS.

        Arguments are ignored, but *args and **kwargs enable support the dbus callback.
        """
        self.playerstatus = self.mprisprops.GetAll('org.mpris.MediaPlayer2.Player')

    def get_status(self):
        data = {'artist': None, 'album': None, 'title': None, 'file': None, 'length': None}

        data['state'] = (self.playerstatus['PlaybackStatus']
                .replace('Stopped', 'stop')
                .replace('Playing', 'play')
                .replace('Paused', 'pause'))
        try:
            data['length'] = round(int(self.playerstatus['Metadata']['mpris:length']) / 1000000)
        except KeyError:
            pass
        try:
            data['artist'] = self.playerstatus['Metadata']['xesam:artist'][0]
        except KeyError:
            pass
        try:
            title = self.playerstatus['Metadata']['xesam:title']
            # According to MPRIS/Xesam, title is a String, but some players seem return an array
            data['title'] = title[0] if isinstance(title, dbus.Array) else title
        except KeyError:
            pass
        try:
            data['album'] = self.playerstatus['Metadata']['xesam:album']
        except KeyError:
            pass
        try:
            data['file'] = self.playerstatus['Metadata']['xesam:url'].split('file://')[1]
        except KeyError:
            pass

        for k in data:
            setattr(self, k, data[k])

    def send_command(self, command):
        if command == 'volup':
            volume = self.playerstatus['Volume'] + 0.1
            self.mprisprops.Set('org.mpris.MediaPlayer2.Player', 'Volume', min(volume, 1.0))
            return True
        if command == 'voldn':
            volume = self.playerstatus['Volume'] - 0.1
            self.mprisprops.Set('org.mpris.MediaPlayer2.Player', 'Volume', max(volume, 0.0))
            return True

        cmd = {
            'play': self.mprisplayer.PlayPause,
            'pause': self.mprisplayer.Pause,
            'next': self.mprisplayer.Next,
            'prev': self.mprisplayer.Previous,
            'stop': self.mprisplayer.Stop,
        }.get(command)
        
        if cmd:
            try:
                cmd()
            except dbus.DBusException:
                # Some players (rhythmbox) raises DBusException when attempt to
                # use "next"/"prev" command on first/last item of the playlist
                pass
            return True
