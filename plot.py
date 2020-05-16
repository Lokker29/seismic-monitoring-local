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

        coords = self._prepare_data_for_map(data)

        ax = coords.plot(zorder=2, markersize=13, figsize=(20, 9))
        world.plot(zorder=1, ax=ax, color='white', edgecolor='black', figsize=(20, 9))

        plt.show()

    def _prepare_data_for_map(self, data, limit=3000):
        coords = []

        for row in data:
            coords.append([row['coord'], row['time']])

        coords = list(sorted(coords, key=lambda x: x[1], reverse=True))

        coords = [coord for coord, _ in coords]

        longitude = [coord[0] for coord in coords[:limit]]
        latitude = [coord[1] for coord in coords[:limit]]

        df = pd.DataFrame({'latitude': latitude, 'longitude': longitude})

        gdf = geopandas.GeoDataFrame(
            df, geometry=geopandas.points_from_xy(df.longitude, df.latitude))

        return gdf

    # def only_usa(self, coords):
    #     usa = {'sw': {'lat': 24.9493, 'lng': -125.0011}, 'ne': {'lat': 49.5904, 'lng': -66.9326}}
    #     alaska = {'sw': {'lat': 49, 'lng': -175}, 'ne': {'lat': 72, 'lng': -128}}
    #     gavaii = {'sw': {'lat': 17, 'lng': -161}, 'ne': {'lat': 23, 'lng': -154}}
    #
    #     regions = {
    #         'usa': usa, 'alaska': alaska, 'gavaii': gavaii
    #     }
    #     result = []
    #
    #     for point, time in coords:
    #         in_region = False
    #
    #         for bounds in regions.values():
    #             sw = bounds['sw']
    #             ne = bounds['ne']
    #             if sw['lng'] < point[0] < ne['lng'] and sw['lat'] < point[1] < ne['lat']:
    #                 in_region = True
    #
    #         if in_region:
    #             result.append((point, time))
    #
    #     return result
