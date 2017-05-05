from api.graph import GraphAPI
from api.currency import CurrencyAPI
from api.messages import MessagesAPI
import config


class Trader:
    def __init__(self):
        self.messagesAPI = MessagesAPI()
        self.currencyAPI = CurrencyAPI()
        self.messagesAPI.start()
        return

    def report(self, data, graphs=False, chat_id=None):
        if chat_id is not None:
            def broadcast(m, _type):
                self.messagesAPI.send_to_user(m, _type, chat_id)
        else:
            def broadcast(m):
                self.messagesAPI.send_to_everyone(m)
        broadcast("Report for the %s : " % config.data_duration)
        for currency in data.keys():
            currency_data = data[currency]
            if config.graph_img and graphs:
                GraphAPI.save_image(currency, currency_data, config.graph_img)
                broadcast(config.graph_img, "image")
            broadcast(currency)
