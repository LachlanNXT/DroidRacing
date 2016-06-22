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
        self.frame_chroma = None
        self.last_yellow_mean = config.FRAME_WIDTH * 0.8
        self.last_blue_mean = config.FRAME_WIDTH * 0.2
        self.desired_steering = 0.5 # 0 = left, 0.5 = center, 1 = right
        self.desired_throttle = 0 # 0 = stop, 0.5 = medium speed, 1 = fastest
        self.h = config.FRAME_HEIGHT
        self.w = config.FRAME_WIDTH

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
            # colour
            blue_mask = self.colour_threshold(chroma, config.BLUE_CHROMA_LOW, config.BLUE_CHROMA_HIGH)
            yellow_mask = self.colour_threshold(chroma, config.YELLOW_CHROMA_LOW, config.YELLOW_CHROMA_HIGH)
            colour_mask = cv2.bitwise_or(blue_mask, yellow_mask)
            colour_mask = cv2.erode(colour_mask, config.ERODE_KERNEL)
            colour_mask = cv2.dilate(colour_mask, config.DILATE_KERNEL)

            # lines
            lines = cv2.HoughLinesP(colour_mask, config.HOUGH_LIN_RES, config.HOUGH_ROT_RES, config.HOUGH_VOTES, config.HOUGH_MIN_LEN, config.HOUGH_MAX_GAP)
            blue_lines = np.array([])
            yellow_lines = np.array([])
            if lines != None:
                for line in lines:
                    x1,y1,x2,y2 = line[0]
                    angle = np.rad2deg(np.arctan2(y2-y1, x2-x1))
                    if config.MIN_LINE_ANGLE < abs(angle) < confi.MAX_LINE_ANGLE:
                        if config.IMSHOW:
                            cv2.line(self.frame, (x1,y1), (x2,y2), (0,0,255), 2)
                        if angle > 0:
                            yellow_lines = np.append(yellow_lines, [x1, x2])
                        elif angle < 0:
                            blue_lines = np.append(blue_lines, [x1, x2])

            # find centre
            blue_mean = self.last_blue_mean
            yellow_mean = self.last_yellow_mean
            if len(blue_lines):
                blue_mean = int(np.mean(blue_lines))
            if len(yellow_lines):
                yellow_mean = int(np.mean(yellow_lines))

            centre = (blue_mean + yellow_mean) / 2

            self.last_blue_mean = blue_mean
            self.last_yellow_mean = yellow_mean

            if config.IMSHOW:
                cv2.circle(self.frame, (centre, self.h - 20), 10, (0,0,255), -1)
                cv2.imshow("colour_mask without noise", colour_mask)
                cv2.imshow("raw frame", self.frame)
                cv2.waitKey(1)

    def grab_frame(self):
        self.frame = self.camera.read()
        self.fps_counter.update()
        self.frame_chroma = self.chromaticity(self.frame)

    def colour_threshold(self, image, low, high):
        return cv2.inRange(image, np.array(low), np.array(high))

    def chromaticity(self, image):
        image = image.astype(np.uint16)
        B = image[:, :, 0]
        G = image[:, :, 1]
        R = image[:, :, 2]
        Y = (B + G + R).astype(float)
        b = B / Y
        g = G / Y
        r = R / Y
        image = np.zeros((self.h, self.w, 3), np.uint8)
        image[:, :, 0] = b * 255
        image[:, :, 1] = g * 255
        image[:, :, 2] = r * 255
        return image

    def get_fps(self):
        self.fps_counter.stop()
        return self.fps_counter.fps()

    def get_steering_throttle(self):
        return self.desired_steering, self.desired_throttle