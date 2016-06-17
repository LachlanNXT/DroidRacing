#!/usr/bin/python3.4

import config
import datetime as dt

def debug(message):
    if config.DEBUG:
        timestamp = dt.datetime.now().strftime("%x-%X: ")
        if (config.DEBUG_MODE == "FILE"):
            with open('droid_log.txt', 'a') as log:
                log.write(timestamp + message + "\n")
        elif (config.DEBUG_MODE == "PRINT"):
            print(timestamp + message + "\n")