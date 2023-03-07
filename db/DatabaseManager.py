from pymongo import MongoClient

class MongoDbManager:
    def __init__(self, collection):
        self.conn = MongoClient(
                                    "mongodb+srv://ykmin:dbrudals@cluster0.zyzescr.mongodb.net/?retryWrites=true&w=majority"
                                    ,uuidRepresentation='standard')
        self.db = self.conn.coins
        self.col = self.db.get_collection(collection)