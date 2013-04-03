====
Lyvi
====

-------------
Lyrics viewer
-------------

:Author: Ondrej Kipila <ok100 at lavabit dot com>
:Version: 1.1.0-git
:Manual section: 1

SYNOPSIS
========

``lyvi [-h] [-c file] [-d] [-v] [command]``

DESCRIPTION
===========

Lyvi is a console lyrics, artist info and guitar tabs viewer. On supported terminals, lyvi can also show artist photos and album art.

OPTIONS
=======
``-h``, ``--help``
    Show help message and exit.
``-c``, ``--config-file file``
    Change the configuration file of lyvi from default ``~/.config/lyvi/lyvi.conf`` to ``file``.
``-d``, ``--debug``
    Enable debug mode. Lyvi will create ``lyvi.log`` file in the current directory.
``-v``, ``--version``
    Print version and exit.
``command``
    Send a command to the connected player. Supported commands are: ``play``, ``pause``, ``next``, ``prev``, ``stop``, ``volup``, ``voldn``.

PLAYER SETUP
============

These players don't work out of box and needs a few simple steps:

Gmusicbrowser
-------------

1. Enable ``MPRIS v2`` plugin (Main > Settings > Plugins)

MPlayer
-------

1. Create fifo::

    mkfifo ~/.mplayer/fifo

2. Add this line to ``~/.mplayer/config``::

    input=file=/home/USER.mplayer/fifo

3. If you're using MPlayer with a front-end (e.g. SMPlayer, UMPlayer...), configure it to save MPlayer log to ``/home/USER/.mplayer/log`` file.
   
   a. For SMPlayer/UMPlayer, this option is located at Options > Preferences > Advanced > Logs > Autosave MPlayer log to file

   b. For standalone MPlayer, you need to run it with the following command-line arguments::

       mplayer -quiet -msglevel all=0 -identify <files> > ~/.mplayer/log

Mpg123
------

1. Lyvi works with mpg123 only if mpg123 output is redirected to ``/tmp/mpg123.log``, e.g::

    mpg123 /some/music/*.mp3 2> /tmp/mpg123.log

Music Player Daemon
-------------------

1. Install ``mpc`` package

2. (Optional) Set ``mpd_config_file`` and ``mpd_host`` configuration options

Pianobar
--------

1. Copy ``eventcmd`` script from ``scripts/pianobar/`` to ``~/.config/pianobar/`` and make it executable.
   If you already have custom ``eventcmd`` script, add ``songstart`` event like in the example script.

2. Add this line to ``~/.config/pianobar/config``::

    event_command = /home/USER/.config/pianobar/eventcmd

3. Create fifo::

    mkfifo ~/.config/pianobar/ctl

Qmmp
----

1. Enable ``MPRIS`` plugin (Settings > Plugins)

Shell-fm
--------

1. Add these lines to ``~/.shell-fm/shell-fm.rc``::

    np-file = /home/YOURUSERNAME/.shell-fm/nowplaying
    np-file-format = %a\%t\%l
    unix = /home/YOURUSERNAME/.shell-fm/socket

VLC Media Player
----------------

1. Tools > Preferences > All > Interface > Main Interfaces: check ``Web``, ``Remote control Interface``

2. Expand ``Main interfaces`` in the left pane, click on the ``RC`` item and check ``Fake TTY``.
   Into ``UINX socket command input`` field, write ``/tmp/vlc.sock``

SHORTCUTS
=========

Normal shortcuts
----------------

``k``/``Up``
    Scroll up
``j``/``Down``
    Scroll down
``Left``/``PgUp``
    Page up
``Right``/``PgDown``
    Page down
``g``/``Home``
    Scroll top
``G``/``End``
    Scroll bottom
``a``
    Toggle between views
``s``
    Toggle between background types
``h``
    Toggle UI visibility
``p``
    Speed up autoscroll
``o``
    Slow down autoscroll
``i``
    Toggle autoscroll
``r``
    Re-download metadata for current view
``q``
    Quit

Player control shortcuts
------------------------

``z``
    Previous track
``x``
    Play
``c``
    Pause
``v``
    Stop
``b``
    Next track
``=``
    Increase volume
``-``
    Decrease volume

CONFIGURATION OPTIONS
=====================

Default path to the configuration file is ``~/.config/lyvi/lyvi.conf``.
Each line has ``key = value`` form. Lines starting with ``#`` are ignored.

``autoscroll`` (parameters: [``True``/``False``]; default value: ``False``)
    Enable autoscroll.

``autoscroll_time`` (parameters: ``<time>``; default value: ``10``)
    Autoscroll each ``<time>`` seconds.

``bg`` (parameters: [``True``/``False``]; default value: ``False``)
    Enable background support.

``bg_local`` (parameters: [``True``/``False``]; default value: ``False``)
    Try to find local background images first.

``bg_opacity`` (parameters: ``<opacity>``; default value: ``0.15``)
    Background opacity. ``<opacity>`` lower than ``1.0`` means darken, higher than ``1.0`` lighten.

``bg_tmux`` (parameters: [``True``/``False``]; default value: ``False``)
    Enable tmux background support.

``bg_tmux_backdrops_pane`` (parameters: ``<pane>``; default value: ``None``)
    Tmux pane where backdrops are displayed. Panes are numbered from 0.

``bg_tmux_backdrops_underlying`` (parameters: [``True``/``False``]; default value: ``True``)
    Set to ``True`` if lyvi is running in the same pane that is used for backdrops.

``bg_tmux_cover_pane`` (parameters: ``<pane>``; default value: ``None``)
    Tmux pane where covers are displayed. Panes are numbered from 0.

``bg_tmux_cover_underlying`` (parameters: [``True``/``False``]; default value: ``True``)
    Set to ``True`` if lyvi is running in the same pane that is used for covers.

``bg_tmux_window_title`` (parameters: ``<title>``; default value: ``None``)
    Tmux window title.

``bg_type`` (parameters: ``<type>``; default value: ``backdrops``)
    Default background type. Possible values are: ``backdrops``, ``cover``.

``color_buttons`` (parameters: ``<color>``; default value: ``-1``)
    Color of player control buttons. Possible values are: -1-255.

``color_status`` (parameters: ``<color>``; default value: ``-1``)
    Statusbar text color. Possible values are: -1-255.

``color_text`` (parameters: ``<color>``; default value: ``-1``)
    Text color. Possible values are: -1-255.

``color_title`` (parameters: ``<color>``; default value: ``7``)
    Title color. Possible values are: -1-255.

``key_autoscroll_faster`` (parameters: ``<key>``; default value: ``p``)
    Speed up autoscroll key.

``key_autoscroll_slower`` (parameters: ``<key>``; default value: ``o``)
    Slow down autoscroll key.

``key_autoscroll_toggle`` (parameters: ``<key>``; default value: ``i``)
    Toggle autoscroll key.

``key_bg_toggle`` (parameters: ``<key>``; default value: ``s``)
    Toggle background type key.

``key_next`` (parameters: ``<key>``; default value: ``b``)
    Player next song key.

``key_pause`` (parameters: ``<key>``; default value: ``c``)
    Player pause key.

``key_play`` (parameters: ``<key>``; default value: ``x``)
    Player play key.

``key_prev`` (parameters: ``<key>``; default value: ``z``)
    Player previous song key.

``key_quit`` (parameters: ``<key>``; default value: ``q``)
    Quit key.

``key_reload_view`` (parameters: ``<key>``; default value: ``r``)
    Reload current view key.

``key_stop`` (parameters: ``<key>``; default value: ``v``)
    Player stop key.

``key_toggle`` (parameters: ``<key>``; default value: ``a``)
    Toggle view key.

``key_ui_hide`` (parameters: ``<key>``; default value: ``h``)
    Hide UI key.

``key_voldn`` (parameters: ``<key>``; default value: ``-``)
    Player volume down key.

``key_volup`` (parameters: ``<key>``; default value: ``=``)
    Player volume up key.

``lang`` (parameters: ``<language>``; default value: ``en``)
    Preferred language for metadata.

``mpd_config_file`` (parameters: ``<file>``; default value: ``n/a``)
    Path to MPD config file. By default, lyvi will first try ``~/.mpdconf``, then ``/etc/mpd.conf``. 

``mpd_host`` (parameters: ``<host>``; default value: ``localhost``)
    MPD host. By default, lyvi will first try to autodetect from ``MPD_HOST`` environment variable.

``mpd_port`` (parameters: ``<port>``; default value: ``6600``)
    MPD port. By default, lyvi will first try to autodetect from ``MPD_PORT`` environment variable.

``player`` (parameters: ``<player>``; default value: ``n/a``)
    Default player. Values are usually named like player executable, e.g. ``cmus``, ``deadbeef-main``.
    Use this option to avoid conflicts when you have more than one player running at the same time.

``save_lyrics`` (parameters: [``True``/``False``]; default value: ``False``)
    Save lyrics to the song directory.

``save_lyrics_format`` (parameters: ``<file>``; default value: ``<filename>.lyric``)
    Lyric file name. You can use ``<filename>``, ``<artist>`` and ``<title>`` variables.

    Examples:

    ``save_lyrics_format = <artist> - <title>.lyric``

    ``save_lyrics_format = .lyrics/<filename>.lyric``
 
``ui_hidden`` (parameters: [``True``/``False``]; default value: ``False``)
    Hide UI by default.

``view`` (parameters: ``<view>``; default value: ``lyrics``)
    Default view. Possible values are: ``lyrics``, ``artistbio``, ``guitartabs``.
