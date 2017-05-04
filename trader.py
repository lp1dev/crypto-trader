#!./env/bin/python

from    rx import Observable, Observer
from    time import sleep
import  matplotlib as mpl
mpl.use('Agg')
import  matplotlib.pyplot as plt
import  dateutil.parser
import  requests
import  json
import  config
import  time
import  telebot

plt.ioff()

go_on = True
coinbase_api = "https://www.coinbase.com/api/v2/"
chats = []
bot = telebot.TeleBot(config.telegram_api_key)

def     send_user(message, _type="message", chat=None):
        if _type is "message":
                bot.send_message(chat, message)
        elif _type is "image":
                photo = open(message, 'rb')
                bot.send_photo(chat, photo)
        
def     send_all_chats(message, _type="message"):
        for chat in chats:
                send_user(message, _type, chat)

@bot.message_handler(commands=['stop'])
def     unregister_chat(message):
        global chats
        chats.remove(message.chat.id)
        bot.reply_to(message, 'Noted. You won\'t get anymore trading messages !')

                        
@bot.message_handler(commands=['start'])
def     register_chat(message):
        global chats
        chats.append(message.chat.id)
        bot.reply_to(message, 'Noted. I\'ll start trading in this conversation !')

@bot.message_handler(commands=['graphs'])
def     trade_graphs(message):
        bot.reply_to(message, handle_data(update_data(), True, message.chat.id))

@bot.message_handler(commands=['help'])
def     help(message):
        bot.reply_to(message, "You can use /start to ask me to start printing trading informations in this thread, /stop to ask me to stop and /graphs to print the last data graphs")

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

def     update_data(in1=0, in2=0):
    data = {}
    for currency in config.currencies.keys():
        data[currency] = {}
        currency_data = get_prices(config.currencies[currency], config.data_duration)
        x, y = parse_data(currency_data['data']['prices'])
        data[currency]['x'] = x
        data[currency]['y'] = y
        data[currency]['average'] = moy(x)
        y, x = smooth_data(y, x, config.ponderation)
        data[currency]['smooth_average'] = moy(x)
        data[currency]['smooth_x'] = x
        data[currency]['smooth_y'] = y
    return data

def     print_graph(title, data):
        plt.clf()
        plt.title(title)
        plt.xlabel("Time")
        plt.ylabel("€")
        plt.plot(data['y'], data['x'])
        plt.plot(data['smooth_y'], data['smooth_x'])
        plt.show()

def     save_image(title, data, filename):
        plt.clf()
        sleep(1)
        plt.title(title)
        plt.xlabel("Time")
        plt.ylabel("€")
        plt.plot(data['y'], data['x'])
        plt.plot(data['smooth_y'], data['smooth_x'])
        plt.savefig(filename)

def     handle_data(data, graphs=False, chat_id=None):
        messages = []
        images = []
        for currency in data.keys():
                last_value = data[currency]['x'][len(data[currency]['x']) - 1]
                variation = round((last_value - data[currency]['average']), 4)
                percentage = (variation / data[currency]['average']) * 100.0
                smooth_variation = round((last_value - data[currency]['smooth_average']), 4)
                smooth_variation = ("+" if smooth_variation >= 0 else "") + str(smooth_variation)
                variation = ("+" if variation >= 0 else "") + str(variation) 
                message = "%s[%i €](%s€ [%i%%])(%s€ mmc)]" %(currency, last_value, variation, percentage, smooth_variation)
                messages.append(message)
                if config.graph:
                        print_graph(currency, data[currency])
                if config.graph_img and graphs and chat_id:
                        save_image(currency, data[currency], config.graph_img)
                        send_user(config.graph_img, "image", chat_id)
                if chat_id:
                        send_user(message, "message", chat_id)
                else:
                        send_all_chats(message)
        return {'messages': messages, 'images': images}
  
def	main():
        Observable.interval(config.interval).map(update_data).subscribe(handle_data)
        bot.polling()
        return 0

if __name__ == '__main__':
        try:
                main()
        except KeyboardInterrupt as e:
                print('Trader stopping...')
