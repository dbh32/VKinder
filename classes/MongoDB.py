from pymongo import MongoClient
from pprint import pprint


class MongoDB:

    def __init__(self, db='vkinder', address='localhost', port=27017):
        client = MongoClient(address, port)
        self.db = client[db]
        self.users_collection = self.db.users

    def mongo_show_users_collection(self):
        for user in self.users_collection.find():
            pprint(user)

    def mongo_drop_users_collection(self):
        self.db.drop_collection(self.users_collection)
