import csv
import random
import math
import operator
import matplotlib.pyplot as plt

class KNN:
    def __init__(self, company_data, split):
        self.split = split
        self.company_data = company_data

    # Utworzenie zestawow testowych i treningowych
    def loadDataset(self, trainingSet=[], testSet=[]):
        csvFile = open(self.company_data + '.csv', 'r')
        lines = csv.reader(csvFile)
        data = list(lines)
        for x in range(len(data) - 1):
            for y in range(4):
                data[x][y] = float(data[x][y])
            if random.random() < self.split:
                trainingSet.append(data[x])
            else:
                testSet.append(data[x])


    # Obliczanie odleglosci pomiedzy sasiadami przy uzyciu wzoru na odleglosc punktow od siebie
    def getDistance(self, instance1, instance2, length):
        distance = 0
        for x in range(length):
            distance = distance + pow((instance1[x] - instance2[x]), 2)
        distance = math.sqrt(distance)
        return distance

    # Okreslanie lokalizacji k podobnych przypadkow danych
    def getNeighbors(self, trainingSet, testInstance, k):
        distances = []
        length = len(testInstance) - 1
        for x in range(len(trainingSet)):
            lng = self.getDistance(testInstance, trainingSet[x], length)
            distances.append((trainingSet[x], lng))
        keys = operator.itemgetter(1)
        distances.sort(key=keys)
        neighbors = []
        for x in range(k):
            neighbors.append(distances[x][0])
        return neighbors

    # Generowanie odpowiedzi ze zbioru instancji danych
    def getResponse(self, neighbors):
        votes = {}
        for x in range(len(neighbors)):
            response = neighbors[x][-1]
            if response in votes:
                votes[response] += 1
            else:
                votes[response] = 1
        keys = operator.itemgetter(1)
        sortedVotes = sorted(iter(votes.items()), key=keys, reverse=1)
        return sortedVotes[0][0]

    # Okreslenie dokladnosci wszystkich przewidywan w formie %
    def getAccuracy(self, testSet, predictions):
        correct = 0
        for x in range(len(testSet)):
            if testSet[x][-1] == predictions[x]:
                correct += 1
        return (correct / len(testSet)) * 100.0

    def main(self):
        # przygotowanie danych
        trainingSet = []
        testSet = []
        self.loadDataset(trainingSet, testSet)
        for x in trainingSet:
            for z in range(5):
                x[z] = (float(x[z]))

        for x in testSet:
            for z in range(5):
                x[z] = (float(x[z]))

        #print(('Training set: ' + repr(len(trainingSet))))
        #print(('Test set: ' + repr(len(testSet))))

        # generowanie przewidywan
        predictions = []
        openPrices = []
        closePrices = []
        days = []
        k = 3
        for x in range(len(testSet)):
            openPrices.append(testSet[x][-4])
            closePrices.append(testSet[x][-1])
            days.append(int(testSet[x][-5]))
            neighbors = self.getNeighbors(trainingSet, testSet[x], k)
            result = self.getResponse(neighbors)
            predictions.append(result)
            #print(('predicited  = ' + repr(result) + ', actual = ' + repr(testSet[x][-1])))
        accuracy = self.getAccuracy(testSet, predictions)
        #print(('Accuracy: ' + str(round(float(repr(accuracy)), 2)) + '%'))

        rmse = 0
        sum_error = 0

        for i in range (len(closePrices)):
            prediction_error = float(predictions[i]) - float(closePrices[i])
            sum_error += (prediction_error ** 2)
        rmse = sum_error / float(len(predictions))

        plt.scatter(days, openPrices, c='#2AE21D', label='Open price', s=10)
        plt.scatter(days, closePrices, c='#ef5423', label='Close price', s=10)
        plt.scatter(days, predictions, c='#143850', label='Predicted price', s=5)
        plt.plot(days, predictions, color='#143850', label='Prediction Line')
        plt.xlabel('Days')
        plt.ylabel('Price in $')
        plt.title(self.company_data + ' Chart' + '\nAccuracy: ' + str(round(float(repr(rmse)), 3)))
        plt.legend()
        plt.show()



