cmus-lyrics
===========

Introduction
------------

A simple lyrics viewer for [C\* Music Player](http://cmus.sourceforge.net/) and [shell-fm](http://nex.scrapping.cc/shell-fm/).

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
- And cmus or shell-fm, of course :)

For Arch Linux users. there is an [AUR package](https://aur.archlinux.org/packages.php?ID=57528)

Configuration
-------------

- For use with shell-fm, add these lines to your ~/.shell-fm/shell-fm.rc:

    np-file = /home/YOURUSERNAME/.shell-fm/nowplaying
	np-file-format = %a | %t

Usage
-----
Simple:

	$ cmus-lyrics
