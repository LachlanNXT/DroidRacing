#!/usr/bin/python3.4

import config
import serial
import threading
import queue
import time
import re

class DroidControlThread(threading.Thread):
    # Handles all communication to Arduino over USB serial
    # DroidControlThread launches a thread such that main control loop is not blocked
    # by communications.
    # Control loop puts throttle and steering commands into a Queue which DroidControlThread
    # will consume.
    def __init__(self, command_queue, lock):
        threading.Thread.__init__(self)
        self.command_queue = command_queue
        self.lock = lock
        self.running = True
        self.arduino = None
        try:
            self.arduino = serial.Serial(port=config.SERIAL_NAME,
                                         baudrate=config.SERIAL_BAUD_RATE,
                                         write_timeout=config.SERIAL_TIMEOUT)
        except serial.SerialException:
            if config.DEBUG:
                print("DroidControlThread: Unable to find serial device")
                print("DroidControlThread: Thread not started")
            self.stop()
        
    def run(self):
        if self.arduino == None:
            return
        if config.DEBUG:
            print("DroidControlThread: Thread started")
        self.execute_commands()
        self.arduino.close()
        if config.DEBUG:
            print("DroidControlThread: Thread stopped")

    def stop(self):
        self.running = False
        if config.DEBUG:
            print("DroidControlThread: Stopping thread")

    def execute_commands(self):
        while self.running:
            self.lock.acquire()
            if not self.command_queue.empty():
                command = self.command_queue.get()
                self.lock.release()
                self.send_command(command)
            else:
                self.lock.release()
            time.sleep(config.QUEUE_SLEEP_TIME)

    def send_command(self, command):
        if self.valid_command(command):
            try:
                self.arduino.write(str.encode(command))
                if config.DEBUG:
                    print("DroidControlThread: command sent: " + command)
            except serial.SerialTimeoutException:
                if config.DEBUG:
                    print("DroidControlThread: Timeout writing command to arduino")
        elif config.DEBUG:
                print("DroidControlThread: Invalid command: " + command)

    # refer to arduino code to see how commands are structured
    def valid_command(self, command):
        match = re.match(r'^(T|S){1}([1-9]{1})([0-9]+)$', command)
        if match:
            return int(match.group(2)) == len(match.group(3))
        else:
            return False
        