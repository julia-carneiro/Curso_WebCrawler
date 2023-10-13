from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os


class DataBase:
    def __init__(self):
        load_dotenv()
        self.noticias = self.connect()

    def connect_db(self):
        client = MongoClient(os.getenv("DB_URI"))
        db = client["noticias"]
        return db.noticias

    def insert_db(self, data: dict):
        query = {"title": data["title"]}
        result = self.noticias.find(query).sort("data_publicacao", -1)
        if result is None:
            return self.noticias.insert_one(data)
        # parei aq
