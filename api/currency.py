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
            data[currency]['variation'] = (prices[0] - prices[len(prices) - 1])
            data[currency]['percentage'] = 100 * (data[currency]['variation'] / prices[0])
            prices = self.moving_average(prices)
            data[currency]['ma_average'] = np.average(prices)
            data[currency]['ma_prices'] = prices
            data[currency]['ma_times'] = self.moving_average(times)
        return data

    @staticmethod
    def moving_average(a, n=config.window):
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return list(ret[n - 1:] / n)

    @staticmethod
    def parse_times_prices(data):
        prices = []
        times = []
        for value in data:
            prices.append(float(value['price']))
            datetime = dateutil.parser.parse(value['time'])
            times.append(int(mktime(datetime.timetuple())))
        return prices, times
