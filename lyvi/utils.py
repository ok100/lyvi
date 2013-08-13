# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import argparse
import subprocess
from threading import Thread


def check_output(command):
    return subprocess.check_output(command, shell=True).decode()


def parse_args():
    parser = argparse.ArgumentParser(prog='lyvi')
    parser.add_argument('command', nargs='?',
        help='send a command to the player and exit')
    parser.add_argument('-c', '--config-file',
        help='path to an alternate config file')
    parser.add_argument('-l', '--list-players',
        help='print a list of supported players and exit', action='store_true')
    parser.add_argument('-v', '--version',
        help='print version information and exit', action='store_true')
    return parser.parse_args()


def running(process):
    return process in check_output('ps -C ' + process)


def thread(target, args=()):
    worker = Thread(target=target, args=args)
    worker.daemon = True
    worker.start()
