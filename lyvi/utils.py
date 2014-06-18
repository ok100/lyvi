# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

"""Common functions used across the whole package."""


import socket
import subprocess as sp
from threading import Thread

from psutil import process_iter


def check_output(command):
    """Return an output of the given command."""
    try:
        return sp.check_output(command, shell=True, stderr=sp.DEVNULL).decode()
    except sp.CalledProcessError:
        return ''


def process_fifo(file, command):
    """Send a command to the given fifo.

    Keyword arguments:
    file -- the path to the fifo file
    command -- the command without newline character at the end
    """
    with open(file, 'w') as f:
        f.write(command + '\n')


def process_socket(sock, command):
    """Send a command to the given socket.

    Keyword arguments:
    file -- the path to the socket
    command -- the command without newline character at the end
    """
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(sock)
        s.send((command + '\n').encode())


def running(process_name):
    """Return True if the given process is running, otherwise return False.

    Keyword arguments:
    process_name -- the name of the process
    """
    for p in process_iter():
        if p.name() == process_name:
            return True
    return False


def thread(target, args=()):
    """Run the given callable object in a new daemon thread.

    Keyword arguments:
    target -- the target object
    args -- a tuple of arguments to be passed to the target object
    """
    w = Thread(target=target, args=args)
    w.daemon = True
    w.start()
