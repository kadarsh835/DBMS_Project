from pymongo import MongoClient
from pprint import pprint
import os

class MongoDBHelper:
    def __init__(self):
        self.connect()

    def connect(self):
        self.client = MongoClient(os.environ.get('MONGO_HOST','localhost'), int(os.environ.get('MONGO_PORT', 27017)))
        db = self.client.faculty
        #test Database Connection
        serverStatusResult = db.command("serverStatus")
        pprint(serverStatusResult)
    
    def updateCV(self, emp_id, about_faculty, research_interests, publications, grants, 
                                    awards, teaching_experience):
        db = self.client.faculty
        document = {
            'emp_id' : emp_id,
            'about_faculty' : about_faculty,
            'research_interests' : research_interests,
            'publications' : publications,
            'grants' : grants,
            'awards' : awards,
            'teaching_experience' : teaching_experience,
        }
        pprint(document)
        error = False
        try:
            print('Trying to insert')
            insertion_id = db.faculty_info.insert_one(document)
            print('insertion Successful')
            return insertion_id
        except Exception as e:
            error = True
            print(e)
            print('Error in inserting')
            return error