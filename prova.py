#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

pin_button = 26 
pin_buzz = 19 

def beep():
    GPIO.output(pin_buzz,GPIO.HIGH)

def stop():
    GPIO.output(pin_buzz,GPIO.LOW)    

from distance_sensor import DistanceSensor
s = DistanceSensor(18,16)
GPIO.setup(pin_buzz, GPIO.OUT)   # Set BeepPin's mode is output
stop()
GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for i in range(1,10):
    distance = s.distance()
print("Distance setup completed.")
button = False
try:
    while True:
        if not GPIO.input(pin_button): 
            button = button ^ True 
            stop()
            while not GPIO.input(pin_button):
                time.sleep(0.5)    
        if not button:
            cur_dist = s.distance()
            delta = distance - cur_dist
            print(delta,cur_dist,distance)
            if (delta > 20):
                print("beep!")
                beep()
except KeyboardInterrupt:
    stop()
    GPIO.cleanup()
