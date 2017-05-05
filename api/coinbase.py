import requests
import json
import config


class CoinbaseAPI:
    @staticmethod
    def get_prices(currency, duration):
        r = requests.get(config.coinbase_api_url + "/prices/%s/historic?period=%s" % (currency, duration))
        try:
            return json.loads(r.text)
        except Exception as e:
            print(e)
