from pymongo import MongoClient
import os

def get_db():
    uri = os.getenv("MONGO_URI", "CONNECTION STRING HERE")
    client = MongoClient(uri)
    return client["DATABASE NAME HERE"]