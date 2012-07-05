lyvi
====

Introduction
------------

A simple command-line lyrics viewer for various audio players.

**Screenshots:**

[![Screenshot](http://ompldr.org/tZWZvdQ "screenshot")](http://ompldr.org/vZWZvdQ)
[![Screenshot](http://ompldr.org/tZWZvcg "screenshot")](http://ompldr.org/vZWZvcg)
[![Screenshot](http://ompldr.org/tZWZvdg "screenshot")](http://ompldr.org/vZWZvdg)

**Supported players:**

- [C\* Music Player](http://cmus.sourceforge.net/)
- [Music Player Daemon](http://mpd.wikia.com/wiki/Music_Player_Daemon_Wiki)
- [shell-fm](http://nex.scrapping.cc/shell-fm/)
- [pianobar](http://6xq.net/projects/pianobar/)
- [MOC](http://moc.daper.net/)
- [MPlayer](http://www.mplayerhq.hu/)
- [VLC Media Player](http://www.videolan.org/vlc/)

**Features:**

- Ncurses UI
- Can display lyrics, artist info and guitar tabs
- Downloads metadata from sites that are supported by [glyr](https://github.com/sahib/glyr)
- Cache for downloaded metadata
- Automatically update when song changes
- Player control with configurable keybindings

**User reviews:**

[stormdragon2976](http://stormdragon.us/?p=251)

Installation
------------

**Requirements:**

- Python
- [glyr](https://github.com/sahib/glyr)

For Arch Linux users. there is an [AUR package](https://aur.archlinux.org/packages.php?ID=57528)

Configuration
-------------

Configuration file is located at `~/.config/lyvi/rc` in the following form:

```
key = value
```

```
Key          | Default value | Description
-------------|---------------|--------------------------------------------------------------------------------
lang         | en            | Preferred language for metadata
view         | lyrics        | Default view. Possible values are: lyrics, artistbio, guitartabs
key_quit     | q             | "Quit" key
key_toggle   | a             | "Toggle between views" key
key_play     | x             | "Play" key
key_pause    | c             | "Pause" key
key_next     | b             | "Next song" key
key_prev     | z             | "Previous song" key
key_stop     | v             | "Stop" key
key_volup    | =             | "Volume up" key
key_voldn    | -             | "Volume down" key
color_title  | 7             | Title color. Possible values are: 0-255, -1 for default terminal color
color_text   | -1            | Text color. Possible values are: 0-255, -1 for default terminal color
color_status | -1            | Statusbar text color. Possible values are: 0-255, -1 for default terminal color
```

### Player configuration

#### cmus

- Works out of box.

#### shell-fm

- Add these lines to your `~/.shell-fm/shell-fm.rc`:

```
np-file = /home/YOURUSERNAME/.shell-fm/nowplaying
np-file-format = %a|%t
unix = /home/YOURUSERNAME/.shell-fm/socket
```

#### pianobar

- Copy [eventcmd](https://raw.github.com/ok100/lyvi/master/scripts/pianobar/eventcmd) script from `scripts/pianobar/` to `~/.config/pianobar/` and make it executable:

```
$ cp scripts/pianobar/eventcmd ~/.config/pianobar/
$ chmod +x ~/.config/pianobar/eventcmd
```

If you already have custom eventcmd script, add songstart event like in the [example script](https://raw.github.com/ok100/lyvi/master/scripts/pianobar/eventcmd).

- Add this line to `~/.config/pianobar/config`:

```
event_command = /home/YOURUSERNAME/.config/pianobar/eventcmd
```

- Create a fifo file:

```
mkfifo ~/.config/pianobar/ctl
```

#### MPD

- Install `mpc` package

#### MOC

- Works out of box.


#### MPlayer

NOTE: Previous/Next/Stop and volume keys will not work if you're using MPlayer front-end

- Add this line to `~/.mplayer/config`:

```
input=file=/home/YOURUSERNAME/.mplayer/fifo
```

- If you're using MPlayer with a front-end (e.g. SMPlayer, UMPlayer...), configure it to save MPlayer log to `/home/YOURUSERNAME/.mplayer/log` file. For SMPlayer/UMPlayer, this option is located at Options -> Preferences -> Advanced -> Logs -> Autosave MPlayer log to file

- For standalone MPlayer, you need to run it with the following command-line switches:

```
mplayer -quiet -msglevel all=0 -identify <file> > ~/.mplayer/log
```

#### VLC Media Player

- Tools -> Preferences -> All -> Interface -> Main interfaces: check "Web", "Remote control interface"
- Expand "Main interfaces" in the left pane, click on the "RC" item and check "Fake TTY". Into "UNIX socket command input" field, write `/tmp/vlc.sock`

Usage
-----
Simple:

	$ lyvi

### Basic keys

```
Key        | Function                             
-----------|--------------------------------------------------
Up/k       | Scroll up                            
Down/j     | Scroll down                          
Left/PgUp  | Page up                              
Right/PgDn | Page down                            
g/Home     | Scroll top                           
G/End      | Scroll bottom                        
a          | Toggle between lyrics, artist info and guitar tab
```

### Player control keys

```
Key        | Function                             | Cmus | Shell-fm | Pianobar | MPD | MOC | MPlayer | VLC 
-----------|--------------------------------------|------|----------|----------|-----|-----|---------|----
z          | Previous track                       | Yes  | No       | No       | Yes | Yes | Yes     | Yes 
x          | Play                                 | Yes  | No       | Yes      | Yes | Yes | Yes     | Yes 
c          | Play/Pause                           | Yes  | Yes      | Yes      | Yes | Yes | Yes     | Yes 
v          | Stop                                 | Yes  | Yes      | Yes      | Yes | Yes | Yes     | Yes 
b          | Next track                           | Yes  | Yes      | Yes      | Yes | Yes | Yes     | Yes 
=          | Increase volume                      | Yes  | Yes      | Yes      | Yes | Yes | Yes     | Yes 
-          | Decrease volume                      | Yes  | Yes      | Yes      | Yes | Yes | Yes     | Yes 
```
