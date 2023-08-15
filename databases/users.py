from pymongo import MongoClient
from plugins.config_reader import read_config

class ColUsers:
    def __init__(self):
        config = read_config(category="databases")
        self.col = MongoClient(host=config["ip"], port=config["port"])[config["db_name"]]["users"]
    def query(self, username: str) -> None | dict:
        data = self.col.find_one(
            {"username": username}, 
            {
                "_id": 0,
                "username": 1,
                "password": 1
                })
        
        return data