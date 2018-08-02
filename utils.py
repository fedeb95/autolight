def normalize_hour(hour,minutes):
    notnorm = hour*60+minutes
    return notnorm / (23*60+59)
    
def normalize(x,maxim,minim):
    return (x-minim) / (maxim-minim)
