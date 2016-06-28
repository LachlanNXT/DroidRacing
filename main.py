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

last_error = 0.0
sumError = 0.0

while True:
    try:
        # only add new steering and throttle commands to queue if
        # they have been updated by vision thread
        newError = vision.get_error()
        if newError != last_error:
            diffError = newError - last_error
            sumError = sumError + newError
            last_error = newError
            Pid = config.Kp*last_error + config.Ki*sumError + config.Kd*diffError
            if Pid>1:
                Pid = 1
            if Pid<0:
                Pid = 0
            throttle = 0;
            set_steering_throttle(Pid, throttle)
            print(diffError, sumError, last_error, Pid)
            time.sleep(config.QUEUE_SLEEP_TIME * 10)

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
