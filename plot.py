from datetime import date

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
