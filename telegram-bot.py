#!./env/bin/python

from api.coinbase import CoinbaseAPI
from api.trader import Trader


def main():
    trader = Trader()
    report = trader.report(['day', 'hour'], accounts=CoinbaseAPI.get_accounts(), graphs=True)
    print(report)
    print(trader.advise(report))
    return 0


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print('Trader stopping...')
