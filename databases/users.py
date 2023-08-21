from pymongo import MongoClient
from plugins.config_reader import read_config

class ColUsers:
    def __init__(self):
        config = read_config(category="databases")
        self.col = MongoClient(host=config["ip"], port=config["port"])[config["db_name"]]["users"]
    
    def query(self, data, recv_filter: dict) -> None | dict:
        data = self.col.find_one(data, recv_filter)
        
        return data