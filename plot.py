import json
from datetime import date
from urllib.request import urlopen

import geopandas
import pandas as pd
import matplotlib.pyplot as plt

TIME_CONSTANT = 1e3


def mean_list(data):
    return sum(data) / len(data)


class SeismicPlot:
    def _statistic_of_states(self, data):
        statistic = {}

        for row in data:
            state = row['place'].split(', ')[-1]
            statistic[state] = statistic.get(state, 0) + 1

        return dict(sorted(statistic.items(), key=lambda x: x[1], reverse=True))

    def _statistic_of_magnitude_by_date(self, data):
        statistic = {}

        for row in data:
            day = date.fromtimestamp(row['time'] / TIME_CONSTANT)
            statistic[day] = statistic.get(day, []) + [row['mag']]

        return dict(sorted(statistic.items(), key=lambda x: x[0]))

    def plot_statistic_of_states(self, data):
        statistic = self._statistic_of_states(data)
        cut_dict = dict(tuple(statistic.items())[:30])

        plt.figure(figsize=(20, 9))
        plt.xticks(rotation=60)
        plt.bar(cut_dict.keys(), cut_dict.values(), color='g')
        plt.show()

    def plot_mean_magnitude_by_date(self, data):
        statistic = self._statistic_of_magnitude_by_date(data)

        statistic = {date_.strftime("%d-%m-%Y"): mean_list(mags) for date_, mags in statistic.items()}

        plt.figure(figsize=(20, 9))
        plt.xticks(rotation=-90)
        plt.plot(tuple(statistic.keys()), tuple(statistic.values()), color='g')
        plt.show()

    def show_map(self, data):
        world = geopandas.read_file(
            geopandas.datasets.get_path('naturalearth_lowres')
        )
        usa = world[world.iso_a3 == 'USA']

        coords = self.prepare_data_for_map(data)

        ax = coords.plot(zorder=2, figsize=(20, 9))
        usa.plot(zorder=1, ax=ax, color='white', edgecolor='black', figsize=(20, 9))

        plt.show()

    def prepare_data_for_map(self, data, limit=1000):
        coords = []

        for row in data:
            coords.append([row['coord'], row['time']])

        coords = list(sorted(coords, key=lambda x: x[1], reverse=True))
        coords = self.only_usa(coords)

        longitude = [coord[0] for coord in coords[:limit]]
        latitude = [coord[1] for coord in coords[:limit]]

        df = pd.DataFrame({'latitude': latitude, 'longitude': longitude})

        gdf = geopandas.GeoDataFrame(
            df, geometry=geopandas.points_from_xy(df.longitude, df.latitude))

        return gdf

    def only_usa(self, coords):
        usa = {'sw': {'lat': 24.9493, 'lng': -125.0011}, 'ne': {'lat': 49.5904, 'lng': -66.9326}}

        result = []

        sw = usa['sw']
        ne = usa['ne']

        for point, _ in coords:
            if sw['lng'] < point[0] < ne['lng'] and sw['lat'] < point[1] < ne['lat']:
                result.append(point)

        return result
