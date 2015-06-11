====
Lyvi
====

--------------------------------------
command-line lyrics (and more!) viewer
--------------------------------------

:Author: Ondrej Kipila ``<ok100 at openmailbox dot org>``
:Version: 2.0-git
:Manual section: 1

SYNOPSIS
========

``lyvi [-h] [-c file] [-l] [-v] [command]``

DESCRIPTION
===========

Lyvi is a lyrics, artist info and guitar tabs viewer. On supported terminals, Lyvi can also
show artist photos and cover images.

OPTIONS
=======
``-h``, ``--help``
    Show help message and exit.
``-c``, ``--config-file file``
    Change the configuration file from default ``$HOME/.config/lyvi/lyvi.conf`` to ``file``.
``-l``, ``--list-players``
    Print a list of supported players and exit.
``-v``, ``--version``
    Print version information and exit.
``command``
    Send a command to the connected player and exit.

    Available commands are:

        - ``play``
        - ``pause``
        - ``next``
        - ``prev``
        - ``stop``
        - ``volup``
        - ``voldn``

    **Note:** Not all commands are supported by all players.

KEY BINDINGS
============

``q``
    Quit

``R``
    Reload background image

``r``
    Reload metadata for current view

``s``
    Toggle background type

``a``
    Toggle view

``h``
    Toggle UI

``Up/k/Mouse wheel``
    Scroll up

``Down/j/Mouse wheel``
    Scroll down

``g``
    Scroll to the top

``G``
    Scroll to the bottom

PLAYER SETUP
============

Players not mentioned here should work out-of-box.

Mpd
---

- *Optional:* Set ``mpd_host``, ``mpd_port`` and ``mpd_config_file`` configuration options (see  CONFIGURATION section below)

Mpg123
------

- Redirect ``mpg123`` output to ``/tmp/mpg123.log``, e.g.::

    mpg123 *.mp3 2> /tmp/mpg123.log

Mplayer
-------

- *Optional:* Set ``mplayer_config_dir`` configuration option (see CONFIGURATION section below)
- Create fifo::

    mkfifo /path/to/mplayer/config/dir/fifo

- Add this line to mplayer configuration file::

    input=file=/path/to/mplayer/config/dir/fifo

- If you're using MPlayer with a front-end (e.g. SMPlayer, UMPlayer...), configure it to save
  MPlayer log to ``/path/to/mplayer/config/dir/log`` file

    a. For SMPlayer/UMPlayer, this option is located at
       Options > Preferences > Advanced > Logs > Autosave MPlayer log to file

    b. For standalone MPlayer, you need to run it with the following command-line arguments::

        mplayer -quiet -msglevel all=0 -identify *.mp3 > /path/to/mplayer/config/dir/log

Pianobar
--------

- Copy ``eventcmd`` script from ``lyvi/data/pianobar/`` to ``~/.config/pianobar/`` and make it executable.
  If you already have custom ``eventcmd`` script, add ``songstart`` event like in the example script.

- Add this line to ``~/.config/pianobar/config``::

    event_command = /home/USER/.config/pianobar/eventcmd

- Create fifo::

    mkfifo ~/.config/pianobar/ctl

Shell-fm
--------

- Add these lines to ``~/.shell-fm/shell-fm.rc``::

    np-file = /home/USER/.shell-fm/nowplaying
    np-file-format = %a|%t|%l|%p
    unix = /home/USER/.shell-fm/socket

CONFIGURATION
=============

Default path to the configuration file is ``$HOME/.config/lyvi/lyvi.conf``.
The configuration file has Python syntax. Basically, each line should contain one configuration option
in the ``option = value`` format.

Options
-------

Each option is in the format ``option [type] (default_value)``.

``autoscroll [bool] (False)``
    Enable autoscroll.

``bg [bool] (False)``
    Enable background. Currently, the background is supported only in urxvt.

``bg_opacity [float] (0.15)``
    Background opacity.

``bg_tmux_backdrops_pane [int or None] (None)``
    A tmux pane where the backdrops are displayed. Panes are numbered from 0.
    To enable tmux support, this option must be set.

``bg_tmux_backdrops_underlying [bool] (False)``
    Set to True if Lyvi is running in the same pane where backdrops are displayed.

``bg_tmux_cover_pane [int or None] (None)``
    A tmux pane where the covers are displayed. Panes are numbered from 0.
    To enable tmux support, this option must be set.

``bg_tmux_cover_underlying [bool] (False)``
    Set to True if Lyvi is running in the same pane where covers are displayed.

``bg_tmux_window_title [str or None] (None)``
    A title of the terminal window running tmux.
    To enable tmux support, this option must be set.

``bg_type ['backdrops' or 'cover'] ('cover')``
    Default background type.

``default_player [str or None] (None)``
    Try to find player specified with this option first.

``default_view ['lyrics' or 'artistbio' or 'guitartabs'] ('lyrics')``
    Default view.

``header_bg [str] ('default')``
    Background color of the header.

``header_fg [str] ('white')``
    Foreground color of the header.

``key_quit [str] ('q')``
    "Quit" key.

``key_reload_bg [str] ('R')``
    "Reload background" key.

``key_reload_view [str] ('r')``
    "Reload current view" key.

``key_toggle_bg_type [str] ('s')``
    "Toggle background type" key.

``key_toggle_views [str] ('a')``
    "Toggle view" key.

``key_toggle_ui [str] ('h')``
    "Toggle UI" key.

``mpd_config_file [str] ('~/.mpdconf' or '/etc/mpd.conf')``
    Path to the mpd configuration file.

``mpd_host [str] (same as MPD_HOST environment variable or 'localhost')``
    Mpd host.

``mpd_port [int] (same as MPD_PORT environment variable or 6600)``
    Mpd port.

``mplayer_config_dir [str] (os.environ['HOME'] + '/.mplayer/')``
    Path to the mplayer configuration directory.

``save_cover [str or None] (None)``
    Path to the saved cover (see below).

``save_lyrics [str or None] (None)``
    Path to the saved lyrics (see below).

``statusbar_bg [str] ('default')``
    Background color of the statusbar.

``statusbar_fg [str] ('default')``
    Foreground color of the statusbar.

``text_bg [str] ('default')``
    Background color of the text.

``text_fg [str] ('default')``
    Foreground color of the text.

``ui_hidden [bool] (False)``
    Hide UI by default.

Metadata saving
---------------
In the ``save_lyrics`` and ``save_cover`` options, the following variables can be used:

    - ``<filename>`` -- current song's file name without the suffix
    - ``<songdir>`` -- current song's directory
    - ``<artist>`` -- current song's artist
    - ``<title>`` -- current song's title
    - ``<album>`` -- current song's album

E.g.::

    save_lyrics = '<songdir>/<filename>.lyric'

Examples
--------

- MPD as a default player, normal background::

    default_player = 'mpd'
    bg = True

- Tmux background, assuming that tmux window title is "music" and both cover and backdrops
  are displayed in the pane 2::

    bg = True
    bg_tmux_window_title = 'music'
    bg_tmux_backdrops_pane = 2
    bg_tmux_cover_pane = 2

- Disable "Quit" and "Toggle UI" keys if Lyvi is running in tmux::

    import os

    if 'TMUX' in os.environ:
        key_quit = None
        key_toggle_ui = None
