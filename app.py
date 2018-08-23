from flask import Flask, render_template,request,redirect,url_for
from light_switch import LightSwitch
from distance import DistanceSensor
from light_sensor import LightSensor
from threading import Thread, Timer, Lock
import utils
import datetime
from config_manager import ConfigManager
from db.dbmanager import DBManager
import pandas as pd
from pandas.io.json import json_normalize
from sklearn import tree
from numpy import array
import pin

manager = ConfigManager.get_instance('./app_config')
REGISTER_TIME=manager.config['register_time']
TRAIN_TIME=manager.config['train_time']
DELETE_DAYS=manager.config['train_days']
override = False
clf=None

def register_data():
    data = get_data()
    data['timestamp'] = datetime.datetime.now().timestamp()
    db.save(data)
    Timer(REGISTER_TIME,register_data).start()

def train():
    data = db.get_all()
    data = pd.DataFrame(list(data))
    labels = data['switch']
    values = data['distance','light','time']
    clf=tree.DecisionTreeClassifier()
    clf=clf.fit(values,labels)

def get_data():
    now = datetime.datetime.now()
    time_of_day = utils.normalize_hour(now.hour,now.minute)
    is_on = ls.is_on()
    distance = dst.distance()
    light = lsens.light_amount()
    return {'time':time_of_day,'switch':is_on,'distance':distance,'light':light}

def delete():
    train()
    oldest = (datetime.datetime.now()-datetime.timedelta(days=DELETE_DAYS)).timestamp()
    db.collection.delete_many({"timestamp":{"$lt":oldest}})

def run():
    while True:
        if not override:
            try:
                data = get_data()
                output=clf.predict(json_normalize(data))
                if output=='True' and not ls.is_on():
                    if light_switch_mylock.acquire():
                        ls.activate()
                        light_switch_mylock.release()
                elif output=='False' and ls.is_on():
                    if light_switch_mylock.acquire():
                        ls.activate()
                        light_switch_mylock.release()
            except Exception:
                pass

pin.config('./pin_config')
db = DBManager('train_data','all')
app = Flask(__name__)
ls = LightSwitch(ch=manager.config["light_switch"],on=False)
lsens = LightSensor(manager.config['light_sensor'])
dst = DistanceSensor(echo=manager.config['echo'],trigger=manager.config['trigger'])
light_switch_mylock = Lock()
#bitton = Button() # not only activable from web

t = Timer(REGISTER_TIME,register_data)
Timer(84600.0,delete).start()
t.start()
if not manager.config['train']:
    thread = Thread(target=run)
    thread.start()

@app.route('/')
def index():
    if ls.is_on():
        return render_template('index.html', image="/static/on.png", override=override)
    else:
        return render_template('index.html', image="/static/off.png", override=override)

@app.route('/activate/')
def light_on():
    light_switch_mylock.acquire()
    ls.activate()
    light_switch_mylock.release()
    return redirect(url_for('index'))

@app.route('/override/')
def over():
    global override
    override = override ^ True
    return redirect(url_for('index'))


if __name__ == '__main__':
    # get config, if train=True don't start nn in a new thread but enable training, otherwise only new thread without training
    app.run(debug=True, host='0.0.0.0')
