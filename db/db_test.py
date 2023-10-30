from pymongo import MongoClient

DB_HOST = "localhost"
DB_PORT = 27017
DB_NAME = "RASP"


def ConnectToDB():
    try:
        client = MongoClient(DB_HOST, DB_PORT)
        db = client[DB_NAME]
        return db
    except Exception:
        print("Failed to connect to the database.")
        return None
