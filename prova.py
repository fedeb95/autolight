#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import _thread
from distance_sensor import DistanceSensor

pin_button = 26 
pin_buzz = 19 

class Automation():

    def __init__(self): 
        GPIO.setmode(GPIO.BCM)
        self.s = DistanceSensor(18,16)
        GPIO.setup(pin_buzz, GPIO.OUT)
        self.stop()
        GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for i in range(1,10):
            self.distance = self.s.distance()
        print("Distance setup completed.")
        self.button = False
        self.lock = _thread.allocate_lock()

    def beep(self):
        GPIO.output(pin_buzz,GPIO.HIGH)

    def stop(self):
        GPIO.output(pin_buzz,GPIO.LOW)    

    def off(self):
        self.lock.acquire()
        self.button = True
        self.stop()
        self.lock.release()

    def on(self):
        self.lock.acquire()
        self.button = False
        self.lock.release()
     
    def run(self):
        try:
            while True:
                if not GPIO.input(pin_button): 
                    self.lock.acquire()
                    self.button = self.button ^ True 
                    self.lock.release()
                    self.stop()
                    while not GPIO.input(pin_button):
                        time.sleep(0.5)    
                if not self.button:
                    cur_dist = self.s.distance()
                    delta = self.distance - cur_dist
                    if (delta > 20):
                        self.beep()
        except KeyboardInterrupt:
            self.stop()
            GPIO.cleanup()
