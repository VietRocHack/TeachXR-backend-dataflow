
import pymongo
import os, datetime

class DatabaseService:
    def __init__(self):
        connection_url = os.getenv('SINGLESTORE_CONNECTION_URL')
        if not connection_url:
            raise ValueError("SINGLESTORE_CONNECTION_URL environment variable not set")
        
        self.client = pymongo.MongoClient(connection_url)
        self.db = self.client.test

    def database_count(self, collection_name: str):
        return self.db[collection_name].count_documents({})
    
    def add_index(self, collection_name: str, index_name: str, desc: bool = False):
        self.db[collection_name].create_index([(index_name, pymongo.DESCENDING if desc else pymongo.ASCENDING)])

    def add_to_database(self, collection_name: str, text, image):
        print(self.db[collection_name].insert_one({"text": text, "image": image, "timestamp": datetime.datetime.now(datetime.timezone.utc)}).inserted_id)

    def get_from_database(self, collection_name: str, columns: list = [], num_rows: int = -1):
        return self.db[collection_name].find({}, columns, limit=num_rows if num_rows > 0 else None)
    
    def get_latest_from_database(self, collection_name: str, columns: list = []):
        return self.db[collection_name].find_one(sort=[("timestamp", pymongo.DESCENDING)], projection=columns)
    
    def clear_database(self, collection_name: str):
        self.db[collection_name].delete_many({})