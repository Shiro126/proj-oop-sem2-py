import numpy as np

"""

Wydaje mi się że będzie potrzebna tablica numpy przechowująca kolejną tablicę numpy

coś takiego, tablica długości ilość warstw, każda warstwa jest typu np.ndarray czyli inną tablicą
np.ndarray(shape=[len(parameters)-1], dtype=np.ndarray')


^ to jest piekne, poniewaz miedzy innymi dlatego nie dzialalo

"""


class NeuralController():
    def __init__(self, parameters):
        """
        Tutaj tworzenie tej tablicy dwuwymiarowych tablic
        """

        self.parameters = parameters
        #self.weights = np.ndarray(shape=[len(parameters) - 1], dtype=np.ndarray)
        #self.perceptron_values = np.ndarray(shape=[len(parameters)], dtype=np.ndarray)
        self.weights = []
        self.perceptron_values = []

        for i in range(len(parameters)-1):
            self.weights.append(np.random.uniform(-1., 1., (parameters[i], parameters[i + 1])))
            print(i,parameters[i], parameters[i+1])

        #for i in range(len(parameters)):
         #   self.perceptron_values.append(np.zeros(shape=parameters[i], dtype=float))


    def control(self, plane_me, plane_enemy, bullets):
        "Tu jakieś ciekawe rzeczy, mnożenie macierzy"
        self.perceptron_values.append([1.,2.])
        print("baby is born")
        print(self.perceptron_values[0])
        for i in range(len(self.parameters) - 1):
            self.perceptron_values.append(np.dot(self.perceptron_values[i], self.weights[i]))
            print(i)
            print("self.perceptron_values[i]    ")
            print(self.perceptron_values[i])
            print("self.weights[i]   ")
            print(self.weights[i])
            print("self.perceptron_values[i + 1]   ")
            print(self.perceptron_values[i + 1])

        print("output")
        print(self.perceptron_values[len(self.parameters)-1])

    def mutate_by_percent(self, percent):
        """creationism FTW"""
        pass

n = NeuralController([2, 3, 4])
n.control (0,0,0)
