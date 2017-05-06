import requests
import json
import config
from coinbase.wallet.client import Client

client = Client(config.coinbase_api_key, config.coinbase_api_secret)


class CoinbaseAPI:
    @staticmethod
    def get_prices(currency, duration):
        r = requests.get(config.coinbase_api_url + "/prices/%s/historic?period=%s" % (currency, duration))
        try:
            return json.loads(r.text)
        except Exception as e:
            print(e)

    @staticmethod
    def get_accounts():
        return client.get_accounts()
