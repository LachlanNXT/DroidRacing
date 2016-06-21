#!/usr/bin/python3.4

import config
from utils import debug
import threading
import time
import cv2
import numpy as np
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS

class DroidVisionThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.fps_counter = FPS().start()
        self.camera = PiVideoStream(resolution=(config.FRAME_WIDTH, config.FRAME_HEIGHT))
        self.camera.start()
        time.sleep(2) # wait for camera to initialise
        self.frame = None
        self.frame_hsv = None
        self.desired_steering = 0.5 # 0 = left, 0.5 = center, 1 = right
        self.desired_throttle = 0 # 0 = stop, 0.5 = medium speed, 1 = fastest

    def run(self):
        debug("DroidVisionThread: Thread started")
        self.vision_processing()
        self.camera.stop()
        cv2.destroyAllWindows()
        debug("DroidVisionThread: Thread stopped")

    def stop(self):
        self.running = False
        debug("DroidVisionThread: Stopping thread")

    def vision_processing(self):
        while self.running:
            self.grab_frame()
            ## HSV
            self.frame_hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            blue_mask = self.colour_threshold(self.frame_hsv, config.BLUE_LOW, config.BLUE_HIGH)
            yellow_mask = self.colour_threshold(self.frame_hsv, config.YELLOW_LOW, config.YELLOW_HIGH)

            # INSERT ALGORITHMS FOR FINDING DESIRED STEERING ANGLE AND THROTTLE HERE
            # put those values into self.desired_steering and self.desired_throttle

            if config.IMSHOW:
                cv2.imshow("blue mask | yellow mask", np.hstack((blue_mask, yellow_mask)))
                cv2.imshow("raw frame", self.frame)
                cv2.waitKey(1)

    def grab_frame(self):
        self.frame = self.camera.read()
        self.fps_counter.update()

    def colour_threshold(self, image, low, high):
        return cv2.inRange(image, np.array(low), np.array(high))

    def get_fps(self):
        self.fps_counter.stop()
        return self.fps_counter.fps()

    def get_steering_throttle(self):
        return self.desired_steering, self.desired_throttle