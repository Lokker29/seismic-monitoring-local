from datetime import datetime

from dateutil.relativedelta import relativedelta


def count_of_state(client, splot, start=datetime.today() - relativedelta(days=50), end=datetime.today()):
    data = client.get_data_by_range_date(start, end, 'place')
    splot.plot_statistic_of_states(data)


def avg_mag(client, splot, start=datetime.today() - relativedelta(days=50), end=datetime.today(), data=None):
    if data is None:
        data = client.get_data_by_range_date(start, end, 'time', 'mag')
    splot.plot_mean_magnitude_by_date(data)


def show_map(client, splot, start=datetime.today() - relativedelta(days=50), end=datetime.today(), data=None):
    if data is None:
        data = client.get_data_by_range_date(start, end, 'place', 'coord', 'time')

    splot.show_map(data)
