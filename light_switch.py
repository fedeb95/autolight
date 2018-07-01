import RPi.GPIO as GPIO
class LightSwitch():
    def __init_(self):
        GPIO.setmode(GPIO.BCM)
        self.on = False 
        self.pin = 2
        GPIO.setup(self.pin, GPIO.OUT)

    def is_on():
        return self.on 

    def activate():
        self.on = self.on ^ True
        #activation logic
        GPIO.output(self.pin,self.on)
