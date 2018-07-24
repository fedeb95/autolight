import RPi.GPIO as GPIO

class DistanceSensor:
    def __init__(self,pin):
        GPIO.setmode(GPIO.BCM)
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)
