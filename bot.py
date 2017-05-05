#!./env/bin/python

from api.trader import Trader
from rx import Observable


def main():
    trader = Trader()
    return 0


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print('Trader stopping...')
