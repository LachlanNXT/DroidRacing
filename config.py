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

# camera and image stuff
CAMERA_WARMUP_TIME = 2
RAW_FRAME_WIDTH = 1000
RAW_FRAME_HEIGHT = 300
ROI_YMIN = int(0.5 * RAW_FRAME_HEIGHT)
ROI_YMAX = int(0.9 * RAW_FRAME_HEIGHT)
ROI_XMIN = int(0.15 * RAW_FRAME_WIDTH)
ROI_XMAX = int(0.85 * RAW_FRAME_WIDTH)

# Hough Line Transform
HOUGH_LIN_RES = 1
HOUGH_ROT_RES = np.pi/180
HOUGH_VOTES = 40
HOUGH_MIN_LEN = 20
HOUGH_MAX_GAP = 10

# line sorting stuff
MIN_LINE_ANGLE = 10
MAX_LINE_ANGLE = 90

# morphological stuff
ERODE_KERNEL = np.ones((2,2), np.uint8)
DILATE_KERNEL = np.ones((5,5), np.uint8)

# Chromaticity thresholds
# format: [b, g, r]
YELLOW_CHROMA_LOW = np.array([0, 90, 90])
YELLOW_CHROMA_HIGH = np.array([70, 130, 130])
BLUE_CHROMA_LOW = np.array([90, 0, 0])
BLUE_CHROMA_HIGH = np.array([130, 100, 100])