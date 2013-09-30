# Copyright (c) 2013 Ondrej Kipila <ok100 at openmailbox dot org>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import subprocess
from threading import Thread

from psutil import process_iter


def check_output(command):
    try:
        return subprocess.check_output(command, shell=True).decode()
    except subprocess.CalledProcessError:
        return ''


def running(process_name):
    for p in process_iter():
        if p.name == process_name:
            return True
    return False


def thread(target, args=()):
    worker = Thread(target=target, args=args)
    worker.daemon = True
    worker.start()
