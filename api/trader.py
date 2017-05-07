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
                report[currency] = {'order': 0}
        return report

    @staticmethod
    def percentages_advise(data):
        activating_percentage = 0.2
        report = {}
        for currency in data.keys():
            report[currency] = {'order': 0}
            for time_span in data[currency].keys():
                currency_data = data[currency][time_span]
                if currency_data['percentage'] >= activating_percentage:
                    report[currency]['order'] -= 1
                elif (-1 * currency_data['percentage']) >= activating_percentage:
                        report[currency]['order'] += 1
        return report

    def report(self, time_spans=None, accounts=None, graphs=False):
        report = {}
        for time_span in time_spans:
            data = self.currencyAPI.fetch(time_span)
            for currency in data.keys():
                if currency not in report.keys():
                    report[currency] = {}
                currency_data = data[currency]
                report[currency][time_span] = currency_data
                if config.graph_img and graphs:
                    GraphAPI.save_image(currency.upper(), currency_data, config.graph_img)
                    report[currency][time_span]['graphs'] = {"message": config.graph_img, "type": "image"}
            for account in accounts['data']:
                currency = account['balance']['currency'].lower()
                if currency in report.keys():
                    report[currency][time_span]['amount'] = account['balance']['amount']
                    actual_value = float(account['balance']['amount']) * \
                                   data[currency]['prices'][len(data[currency]['prices']) - 1]
                    passed_value = float(account['balance']['amount']) * \
                                    data[currency]['prices'][0]
                    report[currency][time_span]['amount_price'] = actual_value
                    report[currency][time_span]['amount_variation'] = passed_value - actual_value
        return report
