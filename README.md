cmus-lyrics
===========

Introduction
------------

A simple lyrics viewer for [C\* Music Player](http://cmus.sourceforge.net/), [shell-fm](http://nex.scrapping.cc/shell-fm/) and [pianobar](http://6xq.net/projects/pianobar/).

**Screenshot:**

[![Screenshot](http://ompldr.org/tZDBjMQ "screenshot")](http://ompldr.org/vZDBjMQ)


**Features:**

- Ncurses UI
- Can display lyrics and artist info
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

Usage
-----
Simple:

	$ cmus-lyrics

### Basic keys

Key        | Function                             
-----------|--------------------------------------
Up/k       | Scroll up                            
Down/j     | Scroll down                          
Left/PgUp  | Page up                              
Right/PgDn | Page down                            
g/Home     | Scroll top                           
G/End      | Scroll bottom                        
a          | Toggle between lyrics and artist info

### Player control keys

Key        | Function                             | Cmus | Shell-fm | Pianobar
-----------|--------------------------------------|------|----------|---------
z          | Previous track                       | Yes  | No       | No
x          | Play                                 | Yes  | No       | No
c          | Play/Pause                           | Yes  | Yes      | No
v          | Stop                                 | Yes  | Yes      | No
b          | Next track                           | Yes  | Yes      | No
=          | Increase volume                      | Yes  | Yes      | No
-          | Decrease volume                      | Yes  | Yes      | No
