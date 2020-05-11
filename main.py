from datetime import datetime

from dateutil.relativedelta import relativedelta

from config import MONGO_DB_HOST, MONGO_DB_USER, MONGO_DB_PASSWORD, MONGO_DB_NAME, BASE_SEISMIC_COLLECTION
from db import DBClient
from plot import SeismicPlot


def connect(client):
	client.connect(host=MONGO_DB_HOST, user=MONGO_DB_USER, password=MONGO_DB_PASSWORD)

	client.set_db(MONGO_DB_NAME)

	client.set_collection(BASE_SEISMIC_COLLECTION)


def main():
	client = DBClient()
	splot = SeismicPlot()

	connect(client)

	# last_day = datetime.today() - relativedelta(days=50)
	# today = datetime.today()

	# data = client.get_data_by_range_date(last_day, today, 'place')
	# print(splot.plot_statistic_of_states(data))

	# data = client.get_data_by_range_date(last_day, today, 'time', 'mag')
	# print(splot.plot_mean_magnitude_by_date(data))


if __name__ == '__main__':
	main()
