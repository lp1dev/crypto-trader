import telebot
import config

bot = telebot.TeleBot(config.telegram_api_key)
chats = []


class MessagesAPI:
    @staticmethod
    def start():
        bot.polling()

    @staticmethod
    def send_to_user(message, _type="message", chat=None):
        if _type is "message" and len(message):
            bot.send_message(chat, message)
        elif _type is "image":
            photo = open(message, 'rb')
            bot.send_photo(chat, photo)

    @staticmethod
    def send_to_everyone(message, _type="message"):
        for chat in chats:
            if len(message):
                MessagesAPI.send_to_user(message, _type, chat)

    @staticmethod
    @bot.message_handler(commands=['stop'])
    def unregister_chat(message):
        chats.remove(message.chat.id)
        bot.reply_to(message, 'Noted. You won\'t get anymore trading messages !')

    @staticmethod
    @bot.message_handler(commands=['start'])
    def register_chat(message):
        chats.append(message.chat.id)
        bot.reply_to(message, 'Noted. I\'ll start trading in this conversation !')

    @staticmethod
    @bot.message_handler(commands=['help'])
    def help(message):
        bot.reply_to(message,
                     """You can use /start to ask me to start printing trading
                     informations in this thread, /stop to ask me to stop and /
                     graphs to print the last data graphs""")
