#!/usr/bin/python3.4
import numpy as np

# global config
DEBUG = True
DEBUG_MODE = "PRINT" # use either PRINT or FILE
IMSHOW = True

# used by Main
MIN_THROTTLE = 1500
MAX_THROTTLE = 2000
MIN_STEERING = 1100
MAX_STEERING = 1900

# used by DroidControl
SERIAL_NAME = '/dev/ttyUSB0'
SERIAL_BAUD_RATE = 115200
SERIAL_TIMEOUT = 0.1 # seconds
QUEUE_SLEEP_TIME = 0.025 # seconds

# used by DroidVision
FRAME_WIDTH = 800
FRAME_HEIGHT = 120
# HSV thresholds
BLUE_HSV_LOW = [164, 24, 100]
BLUE_HSV_HIGH = [178, 40, 255]
YELLOW_HSV_LOW = [35, 58, 100]
YELLOW_HSV_HIGH = [40, 80, 255]
# Hough Line Transform
HOUGH_LIN_RES = 1
HOUGH_ROT_RES = np.pi/180
HOUGH_VOTES = 40
HOUGH_MIN_LEN = 20
HOUGH_MAX_GAP = 10
# line sorting stuff
MIN_LINE_ANGLE = 20
MAX_LINE_ANGLE = 90
# morphological stuff
ERODE_KERNEL = np.ones((2,2), np.uint8)
DILATE_KERNEL = np.ones((5,5), np.uint8)

# Chromaticity thresholds
# format: [b, g, r]
YELLOW_CHROMA_LOW = [0, 90, 90]
YELLOW_CHROMA_HIGH = [70, 130, 130]
BLUE_CHROMA_LOW = [90, 0, 0]
BLUE_CHROMA_HIGH = [130, 100, 100]