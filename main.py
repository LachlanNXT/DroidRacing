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
    throttle = int((throttle * (config.MAX_THROTTLE - config.MIN_THROTTLE)) + config.MIN_THROTTLE)
    steering = int((steering * (config.MAX_STEERING - config.MIN_STEERING)) + config.MIN_STEERING)
    st_command = "S" + str(len(str(steering))) + str(steering)
    th_command = "T" + str(len(str(throttle))) + str(throttle)
    lock.acquire()
    command_queue.put(st_command)
    command_queue.put(th_command)
    lock.release()

debug("Main: program starting")

lock = threading.Lock()
command_queue = queue.Queue(50)
droid = DroidControl.DroidControlThread(command_queue, lock)
droid.start()

vision = DroidVision.DroidVisionThread()
vision.start()

last_steering = 0.5
last_throttle = 0

while True:
    try:
        # only add new steering and throttle commands to queue if
        # they have been updated by vision thread
        steering, throttle = vision.get_steering_throttle()
        if steering != last_steering || throttle != last_throttle:
            set_steering_throttle(steering, throttle)
            last_steering = steering
            last_throttle = throttle
    except KeyboardInterrupt:
        debug("Main: KeyboardInterrupt - stopping")
        break

# end program and cleanup
set_steering_throttle(0.5, 0)
debug("Main: Average FPS: " + str(vision.get_fps()))
debug("Main: joining threads")
vision.stop()
command_queue.join()
droid.stop()
droid.join()
vision.join()
debug("Main: program finished")