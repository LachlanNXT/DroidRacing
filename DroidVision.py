#!/usr/bin/python3.4

import config
import threading

class DroidVisionThread(threading.Thread):
    def __init__(self, command_queue, lock):
        threading.Thread.__init__(self)
        