#!/usr/bin/python3.4

import config
import DroidControl
import threading
import queue
import time
import random

lock = threading.Lock()
command_queue = queue.Queue(50)
droid = DroidControl.DroidControlThread(command_queue, lock)
droid.start()

while True:
    lock.acquire()
    command_queue.put("S4" + str(random.randint(1100, 1800)))
    command_queue.put("S4" + str(random.randint(1100, 1800)))
    lock.release()
    time.sleep(5)

command_queue.join()
droid.stop()
droid.join()