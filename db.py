from datetime import timedelta

from pymongo import MongoClient

TIME_CONSTANT = 1e3


class DBClient:
    client = None
    db = None
    collection = None

    def connect(self, host, user, password):
        self.client = MongoClient(
            host=host,
            username=user,
            password=password,
        )

    def set_db(self, name):
        self.db = self.client[name]

    def set_collection(self, name):
        self.collection = self.db[name]

    def get_data_by_date(self, date):
        start = date.timestamp() * TIME_CONSTANT
        end = (date + timedelta(days=1)).timestamp() * TIME_CONSTANT

        return self.collection.find({'time': {'$gte': start, '$lt': end}})
