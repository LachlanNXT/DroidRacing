#!/usr/bin/python3.4

import config
from utils import debug
import threading
import ctypes
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
        self.mean_angle = 0.0
        self.desired_steering = config.NEUTRAL_STEERING # 0 = left, 0.5 = center, 1 = right
        self.desired_throttle = config.NEUTRAL_THROTTLE # 0 = stop, 0.5 = medium speed, 1 = fastest
        self.chromaticity = ctypes.cdll.LoadLibrary('/home/pi/DroidRacing/libchromaticity.so').chromaticity

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

            # magic edge detection
            #median = np.median(self.frame_chroma)
            #lower = int(max(0, (1.0 - config.SIGMA) * median))
            #upper = int(min(255, (1.0 + config.SIGMA) * median))
            #edges = cv2.Canny(self.frame_chroma, lower, upper)
            #cv2.imshow("edges", edges)

            #edges = cv2.dilate(edges, config.BIG_KERNEL, iterations=1)
            #edges = cv2.erode(edges, config.BIG_KERNEL, iterations=1)
            #edges = cv2.erode(edges, config.SMALL_KERNEL, iterations=1)

            #yellow_angle_sum = 0
            #yellow_angle_count = 0
            #blue_angle_sum = 0
            #blue_angle_count = 0
            #if lines != None:
            #    for line in lines:
            #        x1,y1,x2,y2 = line[0]
            #        angle = np.rad2deg(np.arctan2(y2-y1, x2-x1))
            #        if config.MIN_LINE_ANGLE < abs(angle) < config.MAX_LINE_ANGLE:
            #            if config.IMSHOW:
            #                cv2.line(self.frame, (x1,y1), (x2,y2), (0,0,255), 1)
            #            if angle > 0:
            #                yellow_angle_sum += angle
            #                yellow_angle_count += 1
            #            elif angle < 0:
            #                blue_angle_sum += angle
            #                blue_angle_count += 1

            # find mean line angles from lines
            #blue_mean = self.last_blue_mean
            #yellow_mean = self.last_yellow_mean
            #if blue_angle_count:
            #    blue_mean = blue_angle_sum / blue_angle_count
            #if yellow_angle_count:
            #    yellow_mean = yellow_angle_sum / yellow_angle_count
            #self.last_blue_mean = blue_mean
            #self.last_yellow_mean = yellow_mean

            # calculate the average angle
            #self.mean_angle = -(yellow_mean + blue_mean) / 2.0

            #if config.IMSHOW:
            #    cv2.imshow("filtered edges", edges)
            #    cv2.imshow("raw frame", self.frame)
            #    cv2.waitKey(1)

    def get_error(self):
        return self.mean_angle

    def grab_frame(self):
        self.fps_counter.update()
        # grab latest frame and index the ROI
        self.frame = self.camera.read()[config.ROI_YMIN:config.ROI_YMAX, config.ROI_XMIN:config.ROI_XMAX]
        # convert to chromaticity colourspace
        self.chromaticity(ctypes.c_void_p(self.frame.ctypes.data), ctypes.c_int(config.NUM_ELEM))

    def get_fps(self):
        self.fps_counter.stop()
        return self.fps_counter.fps()

    def get_steering_throttle(self):
        return self.desired_steering, self.desired_throttle

if __name__ == "__main__":
    v = DroidVisionThread()
    v.start()
    time.sleep(5)
    v.stop()
    print(v.get_fps())
