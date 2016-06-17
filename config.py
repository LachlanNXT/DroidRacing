#!/usr/bin/python3.4

# global config
DEBUG = True
DEBUG_MODE = "FILE" # use either PRINT or FILE
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
QUEUE_SLEEP_TIME = 0.01 # seconds

# used by DroidVision
FRAME_WIDTH = 500
FRAME_HEIGHT = 200
# HSV thresholds
BLUE_LOW = [105, 50, 50]
BLUE_HIGH = [125, 255, 255]
YELLOW_LOW = [25, 130, 130]
YELLOW_HIGH = [38, 255, 255]

