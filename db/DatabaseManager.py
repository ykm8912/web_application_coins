from pymongo import MongoClient

class MongoDbManager:
    def __init__(self, collection):
        self.conn = MongoClient('127.0.0.1', 27018)
        self.db = self.conn.coins
        self.col = self.db.get_collection(collection)