from csv import reader
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import itertools


class PolyInter:
    days = []
    prices = []
    data_set = list()
    split = 0

    def __init__(self, company_data, split):
        self.split = split
        self.company_data = company_data
        self.load_csv()
        self.days_values()

    def load_csv(self):
        self.data_set = list()
        with open(self.company_data + '.csv', 'r') as file:
            csv_reader = reader(file)
            for row in csv_reader:
                if not row:
                    continue
                self.data_set.append(row)
        return self.data_set

    def days_values(self):
        for d in self.data_set:
            self.days.append(int(d[0]))
            self.prices.append(float(d[4]))

    def second_degree_pol(self, days, values):
        return np.polyfit(days, [int(float(value)) for value in values], 2)

    def third_degree_pol(self, days, values):
        return np.polyfit(days, [int(float(value)) for value in values], 3)

    def rmse_metric(self, predicted, actual):
        sum_error = 0.0
        for i in range(len(actual)):
            prediction_error = float(predicted[i]) - float(actual[i])
            sum_error += (prediction_error ** 2)
        mean_error = sum_error / float(len(actual))
        return sqrt(mean_error)

    def make_predictions(self):
        pre_set = np.linspace(int(len(self.days) * self.split), len(self.days),
                              len(self.days) - int(len(self.days) * self.split))

        predictions_2 = np.polyval(self.second_degree_pol(self.days[:int(len(self.days)*self.split)], self.prices[:int(len(self.prices)*self.split)]), pre_set)

        targets = self.prices[int(len(self.days) * self.split):]

        rmse_2 = self.rmse_metric(predictions_2, targets)

        return rmse_2

    def plots(self):
        training_days = self.days[:int(len(self.days) * self.split)]
        training_prices = self.prices[:int(len(self.prices) * self.split)]

        testing_days = self.days[int(len(self.days) * self.split):]
        testing_prices = self.prices[int(len(self.prices) * self.split):]

        plt.scatter(training_days, training_prices, c='#ecb123', label='Training Prices')
        plt.scatter(testing_days, testing_prices, c='#c53ace', label='Testing Prices')

        xp = np.linspace(0, len(self.days), len(self.days))

        plt.plot(xp, np.polyval(self.second_degree_pol(self.days[:int(len(self.days)*self.split)], self.prices[:int(len(self.prices)*self.split)]), xp), 'g--', label='2nd degree pred')
        plt.xlabel('Days')
        plt.ylabel('Prices in $')
        plt.legend()
        plt.title(self.company_data + ' Chart' + '\nAccuracy: 2nd degree: ' + str(round(self.make_predictions(), 3)))
        plt.show()
