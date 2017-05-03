#!/bin/python

from    rx import Observable, Observer
import  matplotlib.pyplot as plt
import  dateutil.parser
import  requests
import  json
import  config
import  time

go_on = True
coinbase_api = "https://www.coinbase.com/api/v2/"

def     moy(x):
    moy = 0
    for value in x:
        moy += value
    return moy / len(x)

def     smooth_data(x, y, p):
    xout=[]
    yout=[]
    xout.append(x[0])
    yout.append(y[0])
    for i in range(p, len(x) - p):
        xout.append(x[i])
    for i in range(p, len(y) - p):
        val = 0
        for k in range(2 * p):
            val += y[i - p + k]
        yout.append(val / 2 / p)
    xout.append(x[len(x) - 1])
    yout.append(y[len(y) - 1])
    return xout, yout

def     get_prices(currency, duration):
  r = requests.get(coinbase_api + "/prices/%s/historic?period=%s" %(currency, duration))
  data = json.loads(r.text)
  return data

def     parse_data(data):
    prices = []
    times = []
    for value in data:
        prices.append(float(value['price']))
        datetime = dateutil.parser.parse(value['time'])
        times.append(int(time.mktime(datetime.timetuple())))
    return prices, times

def     update_data(in1, in2):
    data = {}
    for currency in config.currencies.keys():
        data[currency] = {}
        currency_data = get_prices(config.currencies[currency], config.data_duration)
        x, y = parse_data(currency_data['data']['prices'])
        data[currency]['x'] = x
        data[currency]['y'] = y
        y, x = smooth_data(y, x, config.ponderation)
        data[currency]['smooth_x'] = x
        data[currency]['smooth_y'] = y
        data[currency]['average'] = moy(x)
    return data

def     print_graph(title, data):
            plt.title(title)
            plt.xlabel("Time")
            plt.ylabel("Euros")
            plt.plot(data['y'], data['x'])
            plt.plot(data['smooth_y'], data['smooth_x'])
            plt.show()    

def     handle_data(data):
    for currency in data.keys():
        print('%s : [%i]' %(currency, data[currency]['average']))
        if config.graph:
            print_graph(currency, data[currency])
  
def	main():
  Observable.interval(config.interval).map(update_data).subscribe(handle_data)
  while go_on:
    True
  return 0

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt as e:
    print('Trader stopping...')
