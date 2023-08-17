from pymongo import MongoClient
from plugins.config_reader import read_config


class ColTicket:
    def __init__(self) -> None:
        config = read_config(category="databases")
        self.col = MongoClient(host=config["ip"], port=config["port"])[config["db_name"]]["ticket"]
    
    def count_total_document(self) -> int:
        return self.col.count_documents(filter={})
    
    def list(self, limit: int = 50, skip: int = 0) -> list[dict[str, str | int]]:
        result = []
        data = self.col.find({}, {"_id": 0}).limit(limit=limit).skip(skip=skip)
        for i in data:
            result.append(i)
        
        return result
        