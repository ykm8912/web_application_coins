from pymongo import MongoClient
from common.config import MONGO_URI

class MongoDbManager:
    def __init__(self, collection):
        self.conn = MongoClient(
                                    MONGO_URI
                                    ,uuidRepresentation='standard')
        self.db = self.conn.coins
        self.col = self.db.get_collection(collection)