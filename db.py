from datetime import timedelta, datetime

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

    def get_data_by_one_day(self, date, *columns):
        start = date
        end = date + timedelta(days=1)

        return self.get_data_by_range_date(start, end, *columns)

    def get_data_by_range_date(self, start, end, *columns):
        start = start.timestamp() * TIME_CONSTANT
        end = end.timestamp() * TIME_CONSTANT

        return self.collection.find(filter={'time': {'$gte': start, '$lt': end}},
                                    projection={column: 1 for column in columns})

    def get_avg_magnitude_today(self):
        collection = self.db['ML-predict']
        md = list(collection.find().sort('_id', -1).limit(1))[0]

        return md['predict']
