from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class Database :
    def __init__(self, database_name) :
        try :
            self.client = MongoClient(os.environ.get('mongourl'))
            self.db = self.client[database_name]
        except OSError or ValueError or Exception as e :
            print(f"database connect error {e}")