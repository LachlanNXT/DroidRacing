#!/usr/bin/python3.4

import config
from utils import debug
import DroidControl
import DroidVision
import threading
import queue
import time
import random
import subprocess

def set_steering_throttle(steering, throttle):
    # convert steering and throttle from 0-1 range to pulse width
    throttle = int((throttle * (config.MAX_THROTTLE - config.MIN_THROTTLE)) + config.MIN_THROTTLE)
    steering = int((steering * (config.MAX_STEERING - config.MIN_STEERING)) + config.MIN_STEERING)
    # build into commands for arduino
    st_command = "S" + str(len(str(steering))) + str(steering)
    th_command = "T" + str(len(str(throttle))) + str(throttle)
    # add to queue for arduino thread to send
    lock.acquire()
    command_queue.put(st_command)
    command_queue.put(th_command)
    lock.release()

debug("Main: DankDroid3000 starting")

# create data structure things
lock = threading.Lock()
command_queue = queue.Queue(50)

# start arduino interface thread
droid = DroidControl.DroidControlThread(command_queue, lock)
droid.start()

# start vision thread
vision = DroidVision.DroidVisionThread()
vision.start()

last_steering = config.NEUTRAL_STEERING
last_throttle = config.NEUTRAL_THROTTLE

while True:
    try:
        # only add new steering and throttle commands to queue if
        # they have been updated by vision thread
        steering, throttle = vision.get_steering_throttle()
        if steering != last_steering || throttle != last_throttle:
            set_steering_throttle(steering, throttle)
            last_steering = steering
            last_throttle = throttle
        time.sleep(config.QUEUE_SLEEP_TIME * 2)
    except KeyboardInterrupt:
        debug("Main: KeyboardInterrupt - stopping")
        break

# end program and cleanup
set_steering_throttle(config.NEUTRAL_STEERING, config.NEUTRAL_THROTTLE)
debug("Main: Average FPS: " + str(vision.get_fps()))
debug("Main: joining threads")
vision.stop()
command_queue.join()
droid.stop()
droid.join()
vision.join()
debug("Main: program finished")