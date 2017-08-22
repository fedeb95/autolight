import datetime

class Environment():
    def is_night():
        time = datetime.datetime.now.hour
        return time > 20 and time < 6
