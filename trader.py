#!./env/bin/python

from    rx import Observable, Observer
from    time import sleep
import  requests
import  json
import  config
import  time
import  telebot
from service import CurrencyAPI

go_on = False
chats = []
bot = None
api = None

def     init():
        global go_on
        global bot
        global api
        go_on = True
        bot = telebot.TeleBot(config.telegram_api_key)
        api = CurrencyAPI()
        bot.polling()

def     send_user(message, _type="message", chat=None):
        if _type is "message" and len(message):
                bot.send_message(chat, message)
        elif _type is "image":
                photo = open(message, 'rb')
                bot.send_photo(chat, photo)
        
def     send_all_chats(message, _type="message"):
        for chat in chats:
                if len(message):
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
        handle_data(update_data(), True, message.chat.id)

@bot.message_handler(commands=['help'])
def     help(message):
        bot.reply_to(message, "You can use /start to ask me to start printing trading informations in this thread, /stop to ask me to stop and /graphs to print the last data graphs")

def     handle_data(data, graphs=False, chat_id=None):
        if chat_id is None:
                send_all_chats("Report for the %s : " %(config.data_duration))
        else:
                send_user("Report for the %s : " %(config.data_duration), "message", chat_id)
        for currency in data.keys():
                last_value = data[currency]['x'][len(data[currency]['x']) - 1]
                variation = round((data[currency]['average'] - last_value), config.digits)
                percentage = round((variation / data[currency]['average']) * 100.0, config.digits)
                smooth_variation = round((data[currency]['smooth_average'] - last_value), config.digits)
                smooth_percentage = round((smooth_variation / data[currency]['smooth_average']) * 100, config.digits)
                smooth_variation = ("+" if smooth_variation >= 0 else "") + str(smooth_variation)
                variation = ("+" if variation >= 0 else "") + str(variation) 
                message = "%s [%s €](%s€ [%s%%])(%s€ mmc [%s%%])" %(currency.upper(), str(last_value), variation, str(percentage), smooth_variation, str(smooth_percentage))
                if config.graph:
                        print_graph(currency, data[currency])
                if config.graph_img and graphs and chat_id:
                        save_image(currency, data[currency], config.graph_img)
                        send_user(config.graph_img, "image", chat_id)
                if chat_id:
                        send_user(message, "message", chat_id)
                else:
                        send_all_chats(message)
  
def	main():
#Observable.interval(config.interval).map(api.fetch).subscribe(handle_data)
        init()
        return 0

if __name__ == '__main__':
        try:
                main()
        except KeyboardInterrupt as e:
                print('Trader stopping...')
