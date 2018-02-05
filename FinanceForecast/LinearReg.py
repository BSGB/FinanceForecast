from csv import reader
from math import sqrt

import matplotlib.pyplot as plt
import numpy as np


class LinearReg(object):
    file_name = ''
    split = 0
    data_set = list()
    data_set_copy = list()
    train = list()
    test = list()

    def __init__(self, file_name, split):
        self.file_name = file_name
        self.split = split
        self.data_set = self.load_csv()
        self.str()

    def str(self):
        for i in range(len(self.data_set[0])):
            self.str_column_to_float(i)

    def load_csv(self):
        with open(self.file_name + '.csv', 'r') as file:
            csv_reader = reader(file)
            for row in csv_reader:
                if not row:
                    continue
                self.data_set.append(row)
        return self.data_set

    def str_column_to_float(self, column):
        for row in self.data_set:
            row[column] = float(row[column].strip())

    def train_test_split(self):
        self.data_set_copy = self.data_set[int(len(self.data_set)*self.split):]
        self.train = self.data_set[:int(len(self.data_set)*self.split)]
        return self.train, self.data_set_copy

    def rmse_metric(self, actual, predicted):
        sum_error = 0.0
        for i in range(len(actual)):
            prediction_error = predicted[i] - actual[i]
            sum_error += (prediction_error ** 2)
        mean_error = sum_error / float(len(actual))
        return sqrt(mean_error)

    def evaluate_algorithm(self, algorithm):
        self.train, self.test = self.train_test_split()
        predicted = algorithm(self.train, self.test)
        actual = [row[-1] for row in self.test]
        rmse = self.rmse_metric(actual, predicted)
        return rmse

    def mean(self, values):
        return sum(values) / float(len(values))

    def covariance(self, x, mean_x, y, mean_y):
        covar = 0.0
        for i in range(len(x)):
            covar += (x[i] - mean_x) * (y[i] - mean_y)
        return covar

    def variance(self, values, mean):
        return sum([(x - mean) ** 2 for x in values])

    def coefficients(self, dataset):
        x = [row[0] for row in self.data_set]
        y = [row[4] for row in self.data_set]
        x_mean, y_mean = self.mean(x[:int(len(dataset)*self.split)]), self.mean(y[:int(len(dataset)*self.split)])
        b1 = self.covariance(x[:int(len(dataset)*self.split)], x_mean, y[:int(len(dataset)*self.split)], y_mean) / self.variance(x[:int(len(dataset)*self.split)], x_mean)
        b0 = y_mean - b1 * x_mean
        return [b0, b1]

    def simple_linear_regression(self, train, test):
        predictions = list()
        b0, b1 = self.coefficients(self.train)
        for row in test:
            yhat = b0 + b1 * row[0]
            predictions.append(yhat)
        return predictions

    def print_rmse(self):
        rmse = self.evaluate_algorithm(self.simple_linear_regression)
        print('RMSE: %.3f' % (rmse))

    def plots(self):
        days = []
        prices = []

        for d in self.data_set:
            days.append(d[0])
            prices.append(d[4])

        max_x = np.max(days)
        min_x = np.min(days)

        x = x = np.linspace(min_x, max_x, 1000)
        y = self.coefficients(self.data_set)[0] + self.coefficients(self.data_set)[1] * x

        training_days = []
        training_prices = []
        testing_days = []
        testing_prices = []

        training_days = days[:(int)(len(days) * self.split)]
        training_prices = prices[:(int)(len(prices) * self.split)]
        testing_prices = prices[(int)(len(prices) * self.split):]
        testing_days = days[(int)(len(days) * self.split):]

        plt.scatter(training_days, training_prices, c='#ef5423', label='Training Prices')
        plt.scatter(testing_days, testing_prices, c='#2AE21D', label='Testing Prices')
        plt.plot(x, y, color='#143850', label='Prediction Line')

        plt.xlabel('Days')
        plt.ylabel('Price in $')
        plt.legend()
        plt.title(self.file_name + ' Chart' + '\nAccuracy: %.3f' % round(
            self.evaluate_algorithm(self.simple_linear_regression), 3))
        plt.show()
