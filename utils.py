#!/usr/bin/python3.4

import config
import datetime as dt

def debug(message):
    timestamp = dt.datetime.now().strftime("%x-%X: ")
    if (DEBUG_MODE == "FILE"):
        with open('droid_log.txt', 'a') as logfile:
            log.write(timestamp + message + "\n")
    elif (DEBUG_MODE == "PRINT"):
        print(timestamp + message + "\n")