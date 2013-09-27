# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import dbus
import dbus.exceptions
import dbus.glib
import dbus.mainloop.glib

from gi.repository import GObject

from lyvi.players import Player
from lyvi.utils import thread


dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
GObject.threads_init()
dbus.glib.init_threads()
loop = GObject.MainLoop()
thread(loop.run)


def find():
    try:
        for name in dbus.SessionBus().list_names():
            if name.startswith('org.mpris.MediaPlayer2.'):
                return Player(name[len('org.mpris.MediaPlayer2.'):])
    except dbus.exceptions.DBusException:
        pass
    return None


def running(name):
    try:
        bus = dbus.SessionBus()
        bus.get_object('org.mpris.MediaPlayer2.%s' % name, '/org/mpris/MediaPlayer2')
        return True
    except dbus.exceptions.DBusException:
        return False


class Player(Player):
    def running(self):
        return running(self.name)

    def __init__(self, name):
        self.name = name
        self.playerstatus = {}
        bus = dbus.SessionBus()
        playerobject = bus.get_object('org.mpris.MediaPlayer2.' + self.name, '/org/mpris/MediaPlayer2')
        self.mprisplayer = dbus.Interface(playerobject, 'org.mpris.MediaPlayer2.Player')
        self.mprisprops = dbus.Interface(playerobject, 'org.freedesktop.DBus.Properties')
        self.mprisprops.connect_to_signal("PropertiesChanged", self.loaddata)
        self.loaddata()

    def loaddata(self, *args, **kwargs):
        self.playerstatus = self.mprisprops.GetAll('org.mpris.MediaPlayer2.Player')

    def get_status(self):
        data = {'artist': None, 'album': None, 'title': None, 'file': None}
        data['state'] = (self.playerstatus['PlaybackStatus']
                .replace('Stopped', 'stop')
                .replace('Playing', 'play')
                .replace('Paused', 'pause'))
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
        try:
            if command == 'play':
                self.mprisplayer.PlayPause()
            elif command == 'pause':
                self.mprisplayer.Pause()
            elif command == 'next':
                self.mprisplayer.Next()
            elif command == 'prev':
                self.mprisplayer.Previous()
            elif command == 'stop':
                self.mprisplayer.Stop()
            elif command == 'volup':
                volume = self.playerstatus['Volume'] + 0.1
                self.mprisprops.Set('org.mpris.MediaPlayer2.Player', 'Volume', min(volume, 1.0))
            elif command == 'voldn':
                volume = self.playerstatus['Volume'] - 0.1
                self.mprisprops.Set('org.mpris.MediaPlayer2.Player', 'Volume', max(volume, 0.0))
        except dbus.DBusException:
            # Some players (rhythmbox) raises DBusException when attempt to
            # use "next"/"prev" command on first/last item of the playlist
            pass
