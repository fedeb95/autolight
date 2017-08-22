STABLE = 0
ENTERING = 1
EXITING = 2

def main():
    GPIO.setmode(GPIO.BCM)
    sensor_passage = DistanceSensor(,)
    sensor_direction = DistanceSensor(,)
    light_switch = LightSwitch()
    env = Environment()
    room = Room()
    try:
        old_passage = sensor_passage.get_distance() 
        old_dir = sensor_direction.get_distance() 
        while True:
            passage = sensor_passage.get_distance()
            direction = sensor_direction.get_distance()
            movement = get_movement(passage,direction,old_passage,old_dir)
            if(movement == ENTERING)
                room.enter()
            else if (movement == EXITING)
                room.exit()
            if(room.is_empty() and light_switch.is_on() and env.is_night())
                light_switch.activate()
            if(room.first and env.is_night() and not light_switch.is_on())
                light_switch.activate()
            if(not room.is_empty and env.is_night and not light_switch.is_on())
                light_switch.activate()
            if(not room.is_empty and not env.is_night and light_switch.is_on())
                light_switch.activate()
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
if __name__ == '__main__':
 
