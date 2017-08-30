#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
from distance_sensor import DistanceSensor

class Automation():
    
    def __init__(): 
        GPIO.setmode(GPIO.BCM)
        pin_self.button = 26 
        pin_buzz = 19 
        s = DistanceSensor(18,16)
        GPIO.setup(pin_buzz, GPIO.OUT)
        stop()
        GPIO.setup(pin_self.button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for i in range(1,10):
            distance = s.distance()
        print("Distance setup completed.")
        self.button = False

    def beep():
        GPIO.output(pin_buzz,GPIO.HIGH)

    def stop():
        GPIO.output(pin_buzz,GPIO.LOW)    

    def off():
        self.button = True

    def on():
        self.button = False
     
    def run():
        try:
            while True:
                if not GPIO.input(pin_self.button): 
                    self.button = self.button ^ True 
                    stop()
                    while not GPIO.input(pin_self.button):
                        time.sleep(0.5)    
                if not self.button:
                    cur_dist = s.distance()
                    delta = distance - cur_dist
                    print(delta,cur_dist,distance)
                    if (delta > 20):
                        print("beep!")
                        beep()
        except KeyboardInterrupt:
            stop()
            GPIO.cleanup()
