import          matplotlib              as mpl
import          matplotlib.pyplot       as plt
import          requests
import          config
import          dateutil.parser

class           graphAPI():
    mpl.use('Agg')
    plt.ioff()

    @static
    def         print_graph(title, data):
        plt.clf()
	plt.title(title)
        plt.xlabel("Time")
        plt.ylabel("€")
        plt.plot(data['y'], data['x'])
        plt.plot(data['smooth_y'], data['smooth_x'])
        plt.show()

    @static
    def         save_image(title, data, filename):
        plt.clf()
        sleep(1)
        plt.title(title)
        plt.xlabel("Time")
        plt.ylabel("€")
        plt.plot(data['y'], data['x'])
        plt.plot(data['smooth_y'], data['smooth_x'])
        plt.savefig(filename)


class           CoinbaseAPI():
    coinbase_api_url = config.coinbase_api_url
    
    def         __init__(self):
        return

    def         get_prices(self, currency, duration):
        r = requests.get(self.coinbase_api_url + "/prices/%s/historic?period=%s" %(currency, duration))
        try:
            data = json.loads(r.text)
        except Exception as e:
            print(e)
        return data

class           CurrencyAPI():
  
    def         __init__(self):
        self.coinbaseAPI = CoinbaseAPI()
        return

    def         fetch(self, duration=config.data_duration):
        data = {}
        for currency in config.currencies.keys():
	    data[currency] = {}
            currency_data = self.coinbaseAPI.get_prices(config.currencies[currency], duration)
            prices, time = self.parse_prices(currency_data['data']['prices'])
            data[currency]['x'] = prices
            data[currency]['y'] = time
            data[currency]['average'] = self.average(x)
            y, x = self.smooth_data(y, x)
            data[currency]['smooth_average'] = self.average(x)
            data[currency]['smooth_x'] = x
            data[currency]['smooth_y'] = y
        return data
    
    def         average(self, values):
        avg = 0
        for value in values:
            avg += value
        return avg / len(value)

    def         smooth_data(self, x, y, p=config.ponderation):
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

    def         parse_prices(self, data):
        prices = []
        times = []
        for value in data:
            prices.append(float(value['price']))
            datetime = dateutil.parser.parse(value['time'])
            times.append(int(time.mktime(datetime.timetuple())))
        return prices, times
