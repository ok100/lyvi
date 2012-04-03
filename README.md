cmus-lyrics
===========

Introduction
------------

A simple lyrics viewer for [C\* Music Player](http://cmus.sourceforge.net/), [shell-fm](http://nex.scrapping.cc/shell-fm/) and [pianobar](http://6xq.net/projects/pianobar/).

**Screenshot:**

[![Screenshot](http://ompldr.org/tZDBjMQ "screenshot")](http://ompldr.org/vZDBjMQ)


**Features:**

- Ncurses UI
- Downloads lyrics from sites that are supported by [glyr](https://github.com/sahib/glyr)
- Cache for downloaded lyrics
- Automatically update when song changes

Installation
------------

**Requirements:**

- Python (2.x)
- [glyr](https://github.com/sahib/glyr)
- And cmus, shell-fm or pianobar of course :)

For Arch Linux users. there is an [AUR package](https://aur.archlinux.org/packages.php?ID=57528)

Configuration
-------------

### cmus

- Works out of box.

### shell-fm

- Add these lines to your ~/.shell-fm/shell-fm.rc:

```
np-file = /home/YOURUSERNAME/.shell-fm/nowplaying
np-file-format = %a | %t
```

### pianobar

- Copy [eventcmd](https://raw.github.com/ok100/cmus-lyrics/master/scripts/pianobar/eventcmd) script from scripts/pianobar/ to ~/.config/pianobar/ and make it executable:

```
$ cp scripts/pianobar/eventcmd ~/.config/pianobar/
$ chmod +x ~/.config/pianobar/eventcmd
```

If you already have custom eventcmd script, modify it to write '$artist | $title' to ~/.config/pianobar/nowplaying file on songstart event like in the example script.

- Add this line to ~/.config/pianobar/config:

```
event_command = /home/YOURUSERNAME/.config/pianobar/eventcmd
```

Usage
-----
Simple:

	$ cmus-lyrics
