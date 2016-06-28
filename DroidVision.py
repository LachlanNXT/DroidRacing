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
        self.camera = PiVideoStream(resolution=(config.RAW_FRAME_WIDTH, config.RAW_FRAME_HEIGHT))
        self.camera.start()
        time.sleep(config.CAMERA_WARMUP_TIME) # wait for camera to initialise
        self.frame = None
        self.frame_chroma = None
        self.last_yellow_mean = 25.0
        self.last_blue_mean = 25.0
        self.desired_steering = config.NEUTRAL_STEERING # 0 = left, 0.5 = center, 1 = right
        self.desired_throttle = config.NEUTRAL_THROTTLE # 0 = stop, 0.5 = medium speed, 1 = fastest

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
            # colour mask
            blue_mask = cv2.inRange(self.frame_chroma, config.BLUE_CHROMA_LOW, config.BLUE_CHROMA_HIGH)
            yellow_mask = cv2.inRange(self.frame_chroma, config.YELLOW_CHROMA_LOW, config.YELLOW_CHROMA_HIGH)
            colour_mask = cv2.bitwise_or(blue_mask, yellow_mask)
            colour_mask = cv2.erode(colour_mask, config.ERODE_KERNEL)
            colour_mask = cv2.dilate(colour_mask, config.DILATE_KERNEL)

            # lines
            lines = cv2.HoughLinesP(colour_mask, config.HOUGH_LIN_RES, config.HOUGH_ROT_RES, config.HOUGH_VOTES, config.HOUGH_MIN_LEN, config.HOUGH_MAX_GAP)

            yellow_angle_sum = 0
            yellow_angle_count = 0
            blue_angle_sum = 0
            blue_angle_count = 0
            if lines != None:
                for line in lines:
                    x1,y1,x2,y2 = line[0]
                    angle = np.rad2deg(np.arctan2(y2-y1, x2-x1))
                    if config.MIN_LINE_ANGLE < abs(angle) < config.MAX_LINE_ANGLE:
                        if config.IMSHOW:
                            cv2.line(self.frame, (x1,y1), (x2,y2), (0,0,255), 1)
                        if angle > 0:
                            yellow_angle_sum += abs(angle)
                            yellow_angle_count += 1
                        elif angle < 0:
                            blue_angle_sum += abs(angle)
                            blue_angle_count += 1

            # find mean line angles from lines
            blue_mean = self.last_blue_mean
            yellow_mean = self.last_yellow_mean
            if blue_angle_count:
                blue_mean = blue_angle_sum / blue_angle_count
            if yellow_angle_count:
                yellow_mean = yellow_angle_sum / yellow_angle_count
            self.last_blue_mean = blue_mean
            self.last_yellow_mean = yellow_mean

            # calculate the angle difference and direction
            centre = abs(yellow_mean - blue_mean)
            if yellow_mean > blue_mean:
                centre = -centre

            # scale angle difference to steering angle
            self.desired_steering = ((centre/30.0)+1)/2.0 # 30 being the max expected angle difference...

            # kill throttle if no lines found
            if blue_angle_count or yellow_angle_count:
                self.desired_throttle = 0.22
            else:
                self.desired_throttle = 0

            if config.IMSHOW:
                # draw white vertical reference line
                cv2.line(self.frame, (config.WIDTH//2, config.HEIGHT-20), ((config.WIDTH//2), config.HEIGHT-120), (255,255,255), 2)
                # draw green calculated steering angle
                cv2.line(self.frame, (config.WIDTH//2, config.HEIGHT-20), ((config.WIDTH//2)+int(100*np.cos(np.deg2rad(centre+90))), int((config.HEIGHT-20)-100*np.sin(np.deg2rad(centre+90)))), (0,255,0), 2)
                cv2.imshow("colour_mask without noise", colour_mask)
                cv2.imshow("raw frame", self.frame)
                cv2.waitKey(1)

    def grab_frame(self):
        self.fps_counter.update()
        # grab latest frame and index the ROI
        self.frame = self.camera.read()[config.ROI_YMIN:config.ROI_YMAX, config.ROI_XMIN:config.ROI_XMAX]
        # convert to chromaticity colourspace
        B = self.frame[:, :, 0].astype(np.uint16)
        G = self.frame[:, :, 1].astype(np.uint16)
        R = self.frame[:, :, 2].astype(np.uint16)    
        Y = 255.0 / (B + G + R)
        b = (B * Y).astype(np.uint8)
        g = (G * Y).astype(np.uint8)
        r = (R * Y).astype(np.uint8)
        self.frame_chroma = cv2.merge((b,g,r))

    def get_fps(self):
        self.fps_counter.stop()
        return self.fps_counter.fps()

    def get_steering_throttle(self):
        return self.desired_steering, self.desired_throttle
