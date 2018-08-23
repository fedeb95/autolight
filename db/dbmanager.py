from pymongo.mongo_client import MongoClient
import pymongo

class DBManager():
    def __init__(self,db,collection,address='127.0.0.1',port=27017):
        self.client = MongoClient(address,port)
        self.db = self.client[db]
        self.collection = self.db[collection]

    def save(self,dic):
        self.collection.insert(dic)
        
    def get_all(self):
        return self.collection.find()

    def get_max(self,attr):
        return self.collection.find_one(sort=[(attr, pymongo.DESCENDING)])

    def get_min(self,attr):
        return self.collection.find_one(sort=[(attr, pymongo.ASCENDING)])
