from pymongo import MongoClient
from plugins.config_reader import read_config

class ColTicket:
    def __init__(self):
        config = read_config(category="databases")
        self.col = MongoClient(host=config["ip"], port=config["port"])[config["db_name"]]["ticket"]

    def list(self, limit: int = 50, skip: int = 0):
        result = self.col.find({}).limit(limit).skip(skip)
        return result
        