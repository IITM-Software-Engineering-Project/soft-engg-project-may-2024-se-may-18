
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
load_dotenv()
uri = os.getenv("MONGO_CONNECTION_URI")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# get db
db = client.get_database('seek-next') 

def get_user_code_collection():
    return db.get_collection('user_code')

def get_code_info_collection():
    return db.get_collection('code_info')

