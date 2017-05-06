from api.graph import GraphAPI
from api.currency import CurrencyAPI
import config


class Trader:
    def __init__(self):
        self.currencyAPI = CurrencyAPI()
        return

    @staticmethod
    def advise(data):
        report = Trader.percentages_advise(data)
        for currency in data.keys():
            if 'order' not in report[currency].keys():
                report[currency] = {'order': 'WAIT'}
        return report

    @staticmethod
    def percentages_advise(data):
        activating_percentage = 0.1
        report = {}
        for currency in data.keys():
            report[currency] = {'order': 'WAIT'}
            for time_span in data[currency].keys():
                currency_data = data[currency][time_span]
                if currency_data['percentage'] >= activating_percentage:
                    if report[currency]['order'] == 'SELL':
                        report[currency]['order'] += '++'
                    else:
                        report[currency]['order'] = 'SELL'
                elif (-1 * currency_data['percentage']) >= activating_percentage:
                    if report[currency]['order'] == 'BUY':
                        report[currency]['order'] += '++'
                else:
                    report[currency]['order'] = 'WAIT'
        return report

    def report(self, time_spans=None, graphs=False):
        if time_spans is None:
            time_spans = ['day', 'hour']
        report = {}
        for time_span in time_spans:
            data = self.currencyAPI.fetch(time_span)
            for currency in data.keys():
                report[currency] = {}
                currency_data = data[currency]
                report[currency][time_span] = currency_data
                if config.graph_img and graphs:
                    GraphAPI.save_image(currency.upper(), currency_data, config.graph_img)
                    report[currency][time_span]['graphs'] = {"message": config.graph_img, "type": "image"}
        return report
