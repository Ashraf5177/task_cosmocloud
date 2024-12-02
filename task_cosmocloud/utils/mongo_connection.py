import os

import pymongo
from gridfs import GridFS
 

MONGO_URI = "mongodb+srv://task_cosmocloud:task_cosmocloud@task-cloudcosmo.zv0c4.mongodb.net/?retryWrites=true&w=majority&appName=task-cloudcosmo"

client = pymongo.MongoClient(MONGO_URI, retryWrites=False)
db = client.cosmocloud  
fs = GridFS(db)  