from flask import Flask, render_template,request
from light_switch import LightSwitch
from distance import DistanceSensor
from light_sensor import LightSensor
from threading import Thread
import pin
from threading import Timer
import utils
import datetime
from nn import NeuralNetwork
from config_manager import ConfigManager

manager = ConfigManager.get_instance('./app_config')
pin.config('./pin_config')
app = Flask(__name__)
ls = LightSwitch(ch=manager.config["light_switch"],on=False)
lsens = LightSensor(manager.config['light_sensor'])
dst = DistanceSensor(echo=manager.config['echo'],trigger=manager.config['trigger'])
#bitton = Button() # not only activable from web


def register_data():
    data = get_data()
    print(data) # call service for storage and training instead

def get_data():
    now = datetime.datetime.now()
    time_of_day = utils.normalize_hour(now.hour,now.minute)
    is_on = ls.is_on()
    distance = dst.distance()
    light = lsens.light_amount()

@app.route('/')
def index():
    if ls.is_on():
        return render_template('index.html', image="/static/on.png")
    else:
        return render_template('index.html', image="/static/off.png")

@app.route('/activate/')
def light_on():
    ls.activate()
    if ls.is_on():
        return render_template('index.html', image="/static/on.png")
    else:
        return render_template('index.html', image="/static/off.png")

def run():
    while True:
        output = nn.think(get_data())
        if output:
            ls.activate

if __name__ == '__main__':
    # get config, if train=True don't start nn in a new thread but enable training, otherwise only new thread without training
    app.run(debug=True, host='0.0.0.0')
    if manager.config['train']:
        Timer(60,register_data).start()
    else:
        thread = Thread(target=run)
        thread.start()
