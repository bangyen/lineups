from pymongo.mongo_client import MongoClient
from pymongo.server_api   import ServerApi

import os

class Database:
    client = None

    def __init__(self, cache):
        client = self.get_client()
        cache  = getattr(client, cache)

        self.cache = cache

    @classmethod
    def get_client(cls):
        name  = os.getenv('MONGODB_NAME')
        user  = os.getenv('MONGODB_USER')
        passw = os.getenv('MONGODB_PASS')
        link  = os.getenv('MONGODB_LINK')

        if cls.client:
            return cls.client[name]

        client = MongoClient(
            f'mongodb+srv://{user}:{passw}@{link}',
            server_api=ServerApi('1')
        )

        cls.client = client
        return client[name]

    def find(self, query):
        find = self.cache.find
        view = find(query)

        return list(view)

    def insert(self, data):
        if not data:
            return

        cache  = self.cache
        insert = cache.insert_many

        return insert(data)
