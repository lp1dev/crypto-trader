#!./env/bin/python

from sys import argv
from api.coinbase import CoinbaseAPI
from api.trader import Trader
from utils.colors import colorize as c
from rx import Observable
from datetime import datetime
import config


def tab(column, length=config.column_length):
    while len(column) <= length:
        column += ' '
    return column


def print_report(report):
    if '--clear' in argv:
        print('\033[2J')
    accounts = {}
    time = ''
    for key in report.keys():
        line = c(key.upper(), 'radish_red') + ' '
        for time_span in report[key].keys():
            price = report[key][time_span]['prices'][len(report[key][time_span]['prices']) - 1]
            percent = c('(%s%%)' % round(report[key][time_span]['percentage'], config.decimals),
                        'highlighted_green' if report[key][time_span]['percentage'] >= 0 else 'highlighted_red')
            column = c('%s[%s€%s]' % (time_span[0].upper(), price, percent), 'white') + '|'
            column += c('ACC', 'blood_blue') + ' '
            column += c('%s€' % (round(report[key][time_span]['amount_price'], config.decimals)), 'white')
            column = tab(column)
            line += column
            if time_span not in accounts.keys():
                accounts[time_span] = 0.0
            accounts[time_span] += report[key][time_span]['amount_price']
            last_update = report[key][time_span]['times'][len(report[key][time_span]['times']) - 1]
            time = datetime.fromtimestamp(int(last_update)).strftime('%d-%m-%Y %H:%M:%S')
        print(line)
    print(c('ACC', 'grass_green'), end=' ')
    for time_span in accounts.keys():
        print(tab(c('%s[%s€]' % (time_span[0].upper(), round(accounts[time_span], config.decimals)), 'white'), 44),
              end='')
    print()
    print(time)


def main():
    go_on = True
    trader = Trader()
    report = trader.report(['week', 'day', 'hour'], accounts=CoinbaseAPI.get_accounts(), graphs=True)
    advise = trader.advise(report)
    print_report(report)
    if '--reload' in argv:
        Observable.interval(config.interval).map(
            lambda a, b: trader.report(config.time_spans, accounts=CoinbaseAPI.get_accounts())) \
            .subscribe(print_report)
        while go_on:
            go_on = True
    return 0


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print('Trader stopping...')
