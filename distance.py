import time
import pin

class DistanceSensor():
    def __init__(self,echo,trigger):
        self.trigger = trigger
        self.echo = echo
        #set pin direction (IN / OUT)
        pin.setup(self.trigger, pin.OUT)
        pin.setup(self.echo, pin.IN)


    def distance(self):
        # set Trigger to HIGH
        pin.output(self.trigger, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        pin.output(self.trigger, False)
     
        StartTime = time.time()
        StopTime = time.time()
     
        # save StartTime
        while pin.input(self.echo) == 0:
            StartTime = time.time()
     
        # save time of arrival
        while pin.input(self.echo) == 1:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
     
        return distance

