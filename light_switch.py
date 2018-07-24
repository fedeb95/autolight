import RPi.GPIO as GPIO
class LightSwitch:
    def __init__(self,pin,on):
        GPIO.setmode(GPIO.BCM)
        self.on = on 
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def is_on(self):
        return self.on 

    def activate(self):
        self.on = self.on ^ True
        #activation logic
        GPIO.output(self.pin,self.on)
