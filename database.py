from pymongo import MongoClient
from dotenv import dotenv_values

__all__ = ("client", "collection")

config = dotenv_values(".env")  
client = MongoClient(config["MONGO_URI"])

db = client['steeleye']

collection = db['trades2']