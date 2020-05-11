from datetime import datetime, date, timedelta

from config import MONGO_DB_HOST, MONGO_DB_USER, MONGO_DB_PASSWORD, MONGO_DB_NAME, BASE_SEISMIC_COLLECTION
from db import DBClient


def main():
	client = DBClient()

	client.connect(host=MONGO_DB_HOST, user=MONGO_DB_USER, password=MONGO_DB_PASSWORD)

	client.set_db(MONGO_DB_NAME)

	client.set_collection(BASE_SEISMIC_COLLECTION)


if __name__ == '__main__':
	main()
