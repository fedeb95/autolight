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
import pin

class Autolight:
    def __init__(self,clf=None):
        self.manager = ConfigManager.get_instance('./app_config')
        self.register_time=self.manager.config['register_time']
        self.train_days=self.manager.config['train_days']
        self.override = False
        self.clf=clf
        if self.clf is None:
            self.clf=tree.DecisionTreeClassifier()
        pin.config('./pin_config')
        self.db = DBManager('train_data','all')
        self.ls = LightSwitch(ch=self.manager.config["light_switch"],on=False)
        self.lsens = LightSensor(self.manager.config['light_sensor'])
        self.dst = DistanceSensor(echo=self.manager.config['echo'],trigger=self.manager.config['trigger'])
        self.light_switch_mylock = Lock()
        #bitton = Button() # not only activable from web
            
    def start(self):
        self.t = Timer(self.register_time,self.register_data,[self])
        Timer(84600.0,self.delete,[self]).start()
        self.t.start()
        if not manager.config['train']:
            self.train()
            thread = Thread(target=self.run,args=self)
            thread.start()

    def register_data(self):
        data = self.get_data()
        data['timestamp'] = datetime.datetime.now().timestamp()
        self.db.save(data)
        Timer(self.register_time,self.register_data,[self]).start()

    def train(self):
        data = self.db.get_all()
        data = pd.DataFrame(list(data))
        labels = data['switch']
        values = data[['distance','light','time']]
        self.clf=self.clf.fit(values,labels)

    def get_data(self):
        now = datetime.datetime.now()
        time_of_day = utils.normalize_hour(now.hour,now.minute)
        is_on = self.ls.is_on()
        distance = self.dst.distance()
        light = self.lsens.light_amount()
        return {'time':time_of_day,'switch':is_on,'distance':distance,'light':light}

    def delete(self):
        self.train()
        oldest = (datetime.datetime.now()-datetime.timedelta(days=self.train_days)).timestamp()
        db.collection.delete_many({"timestamp":{"$lt":oldest}})

    def exclude_switch(self,data):
        return data.loc[:,['distance','light','time']]

    def run(self):
        while True:
            if not self.override:
                try:
                    data = self.get_data()
                    output=self.clf.predict(exclude_data(json_normalize(data)))
                    logging.info("predicted:{}\n".format(output))
                    if output=='True' and not ls.is_on():
                        if self.light_switch_mylock.acquire():
                            self.ls.activate()
                            self.light_switch_mylock.release()
                    elif output=='False' and self.ls.is_on():
                        if self.light_switch_mylock.acquire():
                            self.ls.activate()
                            self.light_switch_mylock.release()
                except Exception as e:
                    logging.error(e) 
