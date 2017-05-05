import config
import dateutil.parser
from time import mktime
from api.coinbase import CoinbaseAPI
import numpy as np


class CurrencyAPI:
    def fetch(self, duration=config.data_duration):
        data = {}
        for currency in config.currencies.keys():
            data[currency] = {}
            currency_data = CoinbaseAPI.get_prices(config.currencies[currency], duration)
            prices, times = self.parse_times_prices(currency_data['data']['prices'])
            data[currency]['prices'] = prices
            data[currency]['times'] = times
            data[currency]['average'] = np.average(prices)
            prices = self.moving_average(prices)
            data[currency]['smooth_average'] = np.average(prices)
            data[currency]['ma_prices'] = prices
        return data

    @staticmethod
    def moving_average(data, window):
        return np.convolve(data, np.ones(window) / window)

    @staticmethod
    def parse_times_prices(data):
        prices = []
        times = []
        for value in data:
            prices.append(float(value['price']))
            datetime = dateutil.parser.parse(value['time'])
            times.append(int(mktime(datetime.timetuple())))
        return prices, times
