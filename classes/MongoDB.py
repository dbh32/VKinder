from pymongo import MongoClient
from pprint import pprint


class MongoDB:

    def __init__(self, db='vkinder', address='localhost', port=27017):
        client = MongoClient(address, port)
        self.db = client[db]
        self.users_collection = self.db.users
        self.top10_collection = self.db.top10

    def mongo_show_collection(self, collection):
        for user in collection.find():
            pprint(user)

    def mongo_drop_collection(self, db, collection):
        db.drop_collection(collection)

    def mongo_insert_many(self, data, collection):
        for item in data:
            collection.insert_many([item])

    def mongo_insert_one(self, data, collection):
        collection.insert_one(data)

    def mongo_get_top10_list(self, collection):
        top10ids = []
        for user in collection.find().sort([('user_score', -1)]).limit(10):
            top10ids.append(user['id'])
        return top10ids
