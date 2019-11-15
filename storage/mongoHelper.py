from pymongo import MongoClient
from pprint import pprint
import os

class MongoDBHelper:
    def __init__(self):
        self.connect()

    def connect(self):
        self.client = MongoClient(os.environ.get('MONGO_HOST','localhost'), int(os.environ.get('MONGO_PORT', 27017)))
        self.db = self.client.faculty
        serverStatusResult=self.db.command("serverStatus")
        pprint(serverStatusResult)