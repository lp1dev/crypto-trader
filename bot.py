#!./env/bin/python

from api.trader import Trader
from api.coinbase import CoinbaseAPI


def main():
    trader = Trader()
    report = trader.report(['day', 'hour'], graphs=True)
    print(report['btc']['hour']['percentage'])
    print(trader.advise(report))
    print(CoinbaseAPI.get_accounts())
    return 0


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print('Trader stopping...')
