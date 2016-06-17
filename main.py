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
    try:
        command = "S4" + str(random.randint(1100, 1800))
        lock.acquire()
        command_queue.put(command)
        lock.release()
        if config.DEBUG:
            print("Main: command added: " + command)
        time.sleep(5)
    except KeyboardInterrupt:
        if config.DEBUG:
            print("Main: main loop ending")
            break

if config.DEBUG:
    print("Main: joining threads")
command_queue.join()
droid.stop()
droid.join()

if config.DEBUG:
    print("Main: finished")