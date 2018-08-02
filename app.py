from flask import Flask, render_template,request
from light_switch import LightSwitch
from distance import DistanceSensor
from light_sensor import LightSensor
from threading import Thread, Timer, Lock
import utils
import datetime
from nn import NeuralNetwork
from config_manager import ConfigManager
from db.dbmanager import DBManager
from numpy import array
import pin

manager = ConfigManager.get_instance('./app_config')
REGISTER_TIME=manager.config['register_time']
TRAIN_TIME=manager.config['train_time']
DELETE_DAYS=manager.config['train_days']

def register_data():
    data = get_data()
    data['timestamp'] = datetime.datetime.now().timestamp()
    db.save(data)
    Timer(REGISTER_TIME,register_data).start()

def train():
    data = db.get_all()
    if not data == None:
        max_distance = db.get_max('distance')['distance']
        min_distance = db.get_min('distance')['distance']
        # split inputs and outputs
        inputs = []
        outputs = []
        for el in data:
            dst = utils.normalize(el['distance'],max_distance,min_distance)
            inputs.append([el['time'],dst,el['light']])
            outputs.append([el['switch']])
        nn.train(array(inputs),array(outputs), 1000)
        with open('weights','w') as f:
            f.write(str(nn.synaptic_weights))
    Timer(TRAIN_TIME,train).start()

def get_data():
    now = datetime.datetime.now()
    time_of_day = utils.normalize_hour(now.hour,now.minute)
    is_on = ls.is_on()
    distance = dst.distance()
    light = lsens.light_amount()
    return {'time':time_of_day,'switch':is_on,'distance':distance,'light':light}

def delete():
    oldest = (datetime.datetime.now()-datetime.timedelta(days=DELETE_DAYS)).timestamp()
    db.collection.delete_many({"timestamp":{"$lt":oldest}})

def run():
    while True:
        try:
            data = get_data()
            max_d = db.get_max('distance')
            min_d = db.get_min('distance')
            if not max_d == None:
                max_d = max_d['distance']
            if not min_d == None:
                min_d = min_d['distance']
            dst = utils.normalize(data['distance'],max_d,min_d)
            output = nn.think(array([data['time'],dst,data['light']]))
            while output and not ls.is_on():
                if light_switch_lock.acquire():
                    ls.activate
                    light_switch_lock.release()
        except Exception:
            pass


pin.config('./pin_config')
db = DBManager('train_data','all')
app = Flask(__name__)
ls = LightSwitch(ch=manager.config["light_switch"],on=False)
lsens = LightSensor(manager.config['light_sensor'])
dst = DistanceSensor(echo=manager.config['echo'],trigger=manager.config['trigger'])
light_switch_lock = Lock()
#bitton = Button() # not only activable from web

nn=NeuralNetwork()

t = Timer(REGISTER_TIME,register_data)
trainer = Timer(TRAIN_TIME,train)
Timer(84600.0,delete).start()
trainer.start()
t.start()
thread = Thread(target=run)
thread.start()

@app.route('/')
def index():
    if ls.is_on():
        return render_template('index.html', image="/static/on.png")
    else:
        return render_template('index.html', image="/static/off.png")

@app.route('/activate/')
def light_on():
    light_switch_lock.acquire()
    ls.activate()
    light_switch_lock.release()
    if ls.is_on():
        return render_template('index.html', image="/static/on.png")
    else:
        return render_template('index.html', image="/static/off.png")
if __name__ == '__main__':
    # get config, if train=True don't start nn in a new thread but enable training, otherwise only new thread without training
    app.run(debug=True, host='0.0.0.0')
