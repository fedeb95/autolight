import pin
class LightSwitch:
    def __init__(self,ch,on):
        pin.setmode(pin.BCM)
        self.on = on 
        self.ch = ch 
        pin.setup(self.ch, pin.OUT)

    def is_on(self):
        return self.on 

    def activate(self):
        self.on = self.on ^ True
        #activation logic
        pin.output(self.ch,self.on)
