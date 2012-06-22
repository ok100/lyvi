cmus-lyrics
===========

Introduction
------------

A simple command-line lyrics viewer for various audio players.

**Screenshots:**

[![Screenshot](http://ompldr.org/tZWZvdQ "screenshot")](http://ompldr.org/vZWZvdQ)
[![Screenshot](http://ompldr.org/tZWZvcg "screenshot")](http://ompldr.org/vZWZvcg)
[![Screenshot](http://ompldr.org/tZWZvdg "screenshot")](http://ompldr.org/vZWZvdg)

**Supported players:**

- [C\* Music Player](http://cmus.sourceforge.net/)
- [MPD](http://mpd.wikia.com/wiki/Music_Player_Daemon_Wiki).
- [shell-fm](http://nex.scrapping.cc/shell-fm/)
- [pianobar](http://6xq.net/projects/pianobar/)

**Features:**

- Ncurses UI
- Can display lyrics, artist info and guitar tabs
- Downloads metadata from sites that are supported by [glyr](https://github.com/sahib/glyr)
- Cache for downloaded metadata
- Automatically update when song changes
- Player control with cmus-like bindings

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

### cmus

- Works out of box.

### shell-fm

- Add these lines to your `~/.shell-fm/shell-fm.rc`:

```
np-file = /home/YOURUSERNAME/.shell-fm/nowplaying
np-file-format = %a|%t
unix = /home/YOURUSERNAME/.shell-fm/socket
```

### pianobar

- Copy [eventcmd](https://raw.github.com/ok100/cmus-lyrics/master/scripts/pianobar/eventcmd) script from `scripts/pianobar/` to `~/.config/pianobar/` and make it executable:

```
$ cp scripts/pianobar/eventcmd ~/.config/pianobar/
$ chmod +x ~/.config/pianobar/eventcmd
```

If you already have custom eventcmd script, add songstart event like in the [example script](https://raw.github.com/ok100/cmus-lyrics/master/scripts/pianobar/eventcmd).

- Add this line to `~/.config/pianobar/config`:

```
event_command = /home/YOURUSERNAME/.config/pianobar/eventcmd
```

### MPD

- Install `mpc` package

Usage
-----
Simple:

	$ cmus-lyrics

### Basic keys

Key        | Function                             
-----------|--------------------------------------------------
Up/k       | Scroll up                            
Down/j     | Scroll down                          
Left/PgUp  | Page up                              
Right/PgDn | Page down                            
g/Home     | Scroll top                           
G/End      | Scroll bottom                        
a          | Toggle between lyrics, artist info and guitar tab

### Player control keys

Key        | Function                             | Cmus | Shell-fm | Pianobar | MPD
-----------|--------------------------------------|------|----------|----------|-----
z          | Previous track                       | Yes  | No       | No       | Yes
x          | Play                                 | Yes  | No       | No       | Yes
c          | Play/Pause                           | Yes  | Yes      | No       | Yes
v          | Stop                                 | Yes  | Yes      | No       | Yes
b          | Next track                           | Yes  | Yes      | No       | Yes
=          | Increase volume                      | Yes  | Yes      | No       | Yes
-          | Decrease volume                      | Yes  | Yes      | No       | Yes
