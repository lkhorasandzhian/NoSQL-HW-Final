from pymongo import MongoClient


MONGO_URI = "mongodb://localhost:27018/"
DB_NAME = "university_db"


def get_database():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]