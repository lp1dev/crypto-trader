import numpy as np
import matplotlib as mpl
from time import sleep

mpl.use('Agg')
import matplotlib.pyplot as plt


class GraphAPI:
    plt.ioff()

    @staticmethod
    def print_graph(title, data):
        plt.clf()
        plt.title(title)
        plt.xlabel("Time")
        plt.ylabel("€")
        plt.plot(data['y'], data['x'])
        plt.plot(data['smooth_y'], data['smooth_x'])
        plt.show()

    @staticmethod
    def save_image(title, data, filename):
        plt.clf()
        sleep(0.5)
        plt.title(title)
        plt.xlabel("Time")
        plt.ylabel("€")
        plt.plot(data['times'], data['prices'])
        plt.plot(data['ma_times'], data['ma_prices'])
        plt.savefig(filename)
