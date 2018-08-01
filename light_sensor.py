import time
import pin

class LightSensor:
    def __init__(self,ch):
        self.ch=ch

    def light_amount(self):
        reading = 0
        pin.setup(self.ch, pin.OUT)
        pin.output(self.ch, pin.LOW)
        time.sleep(0.1)
        pin.setup(self.ch, GPIO.IN)
        # This takes about 1 millisecond per loop cycle
        while pin.input(self.ch) == pin.LOW:
            reading += 1
        return reading
