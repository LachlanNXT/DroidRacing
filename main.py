#!/usr/bin/python3.4

import config
from utils import debug
import DroidControl
import DroidVision
import threading
import queue
import time
import random

def set_steering_throttle(steering, throttle):
    throttle = (throttle * (config.MAX_THROTTLE - config.MIN_THROTTLE)) + MIN_THROTTLE
    steering = (steering * (config.MAX_STEERING - config.MIN_STEERING)) + MIN_STEERING
    st_command = "S" + str(len(str(steering))) + str(steering)
    th_command = "T" + str(len(str(throttle))) + str(throttle)
    lock.acquire()
    command_queue.put(st_command)
    command_queue.put(th_command)
    lock.release()

lock = threading.Lock()
command_queue = queue.Queue(50)
droid = DroidControl.DroidControlThread(command_queue, lock)
droid.start()

vision = DroidVisionThread()
vision.start()

while True:
    steering, throttle = vision.get_steering_throttle()
    set_steering_throttle(steering, throttle)

debug("Main: joining threads")
command_queue.join()
droid.stop()
droid.join()
debug("Main: program finished")