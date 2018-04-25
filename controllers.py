from abc import ABC, abstractmethod
from planes import DIRECTION
from pygame.locals import *
import copy
import numpy as np
import random
import math
import pandas
import constants
import json
import os

class BaseController(ABC):
    """
    A class which will be used as a template for a plane controller.
    Every other controller we will create will inherit from this BaseController,
    to make sure the proper methods are implemented.
    It's not really a big deal since we have only 2 methods.. but trying to learn best practices is not a bad thing
    """

    @abstractmethod
    def control(self, plane_me, plane_enemy, bullets):
        """
        :param plane_me: Plane-type, my plane that the controller will fly and control
        :param plane_enemy: Plane-type, that's the guy i'm trying to kill, needed to get his position, speed and angle
        :param bullets: array, used to determine the position of bullets so we can dodge them
        :return: None
        We pass the plane and the enemy, analyze the data we got,
        then we will call methods such as turn and shoot on our plane object
        """

    @abstractmethod
    def mutate_by_percent(self, percent):
        """This is required because of the evolutionary nature of our algorithm"""
        pass


class HumanController(BaseController):
    def control(self, plane_me, plane_enemy, bullets):
        pass

    def mutate_by_percent(self, percent):
        pass

    def steer(self, keys, plane_me):
        """
        :param keys:
        :param plane_me:
        """
        if keys[K_LEFT]:
            plane_me.turn(DIRECTION.LEFT)

        elif keys[K_RIGHT]:
            plane_me.turn(DIRECTION.RIGHT)

        if keys[K_SPACE]:
            plane_me.shoot()


class DummyController(BaseController):  # Let's try using our template for som real stuff
    def __init__(self):
        print("initialized")

    def control(self, plane_me, plane_enemy, bullets):
        plane_me.turn(DIRECTION.LEFT)
        plane_me.shoot()  # Let me know if you can give that strategy a cool name

    def mutate_by_percent(self, percent):
        """creationism FTW"""
        pass


def sigmoid(x, multiplier=5):
    """
    :param x: what to put into sigmoid function
    :param multiplier: the value that x will be multiplied by, default value is one
    :return: 1 / (1 - math.exp(-x * multiplier))
    """
    return 1 / (1 + math.exp(-x * multiplier))


class NeuralController(BaseController):

    def __init__(self, parameters):
        """
        Tutaj tworzenie tej tablicy dwuwymiarowych tablic
        """
        self.weights_count = 0

        self.parameters = parameters
        self.weights = np.ndarray(shape=[len(parameters) - 1], dtype=np.ndarray)
        self.perceptron_values = np.ndarray([len(parameters)], dtype=np.ndarray)

        for i in range(len(parameters) - 1):
            self.weights[i] = (np.random.uniform(-1., 1., (parameters[i], parameters[i + 1])))
            self.weights_count += parameters[i] * parameters[i + 1]

        for i in range(len(parameters)):
            self.perceptron_values[i] = np.zeros([parameters[i]], dtype=float)

    @staticmethod
    def normalize(current_value, maximum_value):
        return 2 * current_value / maximum_value - 1  # try to simplify this: (value-(max/2))/(max/2)

    def control(self, plane_me, plane_enemy, bullets):
        self.perceptron_values[0][0] = sigmoid(self.normalize(plane_me.plane_body.position[0], constants.SCREEN_WIDTH))
        self.perceptron_values[0][1] = sigmoid(self.normalize(plane_me.plane_body.position[1], constants.SCREEN_HEIGHT))
        self.perceptron_values[0][2] = sigmoid(self.normalize(plane_me.plane_body.angle, 3.14))
        self.perceptron_values[0][3] = sigmoid(self.normalize(plane_me.speed, constants.PLANE_MAX_SPEED))
        self.perceptron_values[0][4] = sigmoid(self.normalize(plane_enemy.plane_body.position[0], constants.SCREEN_WIDTH))
        self.perceptron_values[0][5] = sigmoid(self.normalize(plane_enemy.plane_body.position[1], constants.SCREEN_HEIGHT))
        self.perceptron_values[0][6] = sigmoid(self.normalize(plane_enemy.plane_body.angle, 3.14))
        self.perceptron_values[0][7] = sigmoid(self.normalize(plane_enemy.speed, constants.PLANE_MAX_SPEED))
        # bullets input left to do
        """for i in range(7,28):
            self.perceptron_values[0][i] = sigmoid(bullets[i-7].bullet_body.position[0])
        for i in range(27, 48):
            self.perceptron_values[0][i] = sigmoid(bullets[i-27].bullet_body.position[1])
        """
        for i in range(len(self.parameters) - 1):
            self.perceptron_values[i + 1] = np.dot(self.perceptron_values[i], self.weights[i])
            for j in range(len(self.perceptron_values[i+1])):  # This cannot be the most efficient way to do this
                self.perceptron_values[i+1][j] = sigmoid(self.perceptron_values[i+1][j])

        if self.perceptron_values[-1][0] > 0.5:
            plane_me.turn(DIRECTION.LEFT)
        else:
            plane_me.turn(DIRECTION.RIGHT)

        if self.perceptron_values[-1][1] > 0.5:
            plane_me.shoot()

        #print(self.perceptron_values[-1])

    def mutate_by_percent(self, percent):
        mutations_count = int(self.weights_count * percent)
        mutated_cells = []
        while len(set(mutated_cells)) < mutations_count:  # set is a collection of unique elements
            current_mutated_cell = self.mutate_random()
            mutated_cells.append(current_mutated_cell)
            print(len(set(mutated_cells)))

    def mutate_random(self):
        mutation_layer = random.randrange(len(self.weights))
        mutation_row = random.randrange(len(self.weights[mutation_layer]))
        mutation_column = random.randrange(len(self.weights[mutation_layer][mutation_row]))
        self.weights[mutation_layer][mutation_row][mutation_column] = random.uniform(-1,1)
        return mutation_layer, mutation_row, mutation_column

    def save_to_json(self, filename):
        data_to_save = []
        weight_list = self.weights.tolist()
        for i in range (len(self.parameters)-1):
            weight_list[i] = weight_list[i].tolist()
        data_to_save.append(weight_list)
        data_to_save.append(self.parameters)
        script_dir = os.path.dirname(__file__)
        folder_dir = "saved_networks/"
        absolute_dir = os.path.join(script_dir, folder_dir, filename)
        with open (absolute_dir, 'w') as outfile:
            json.dump(data_to_save, outfile)

    def load_from_json(self, filename):
        self.parameters = []
        with open (filename) as infile:
            loaded_data = json.load(infile)
        new_weight_list = loaded_data[0]
        self.weights = np.array(new_weight_list)
        self.parameters = loaded_data[1]
        for i in range(len(self.parameters) - 1):
            self.weights[i] = np.array(self.weights[i])

class EvolutionController:
    """
    Now that's a different type of a controller.
    This baby will take care of model evaluation and breeding.
    She will just give us subjects to test, we will give her points for them.
    When all models are evaluated, we will rank them and breed the best one.
    If you don't remember what I'm talking about check the todo.md file
    """

    def __init__(self, controller_type, population_count):
        """
        :param controller_type: inherits from BaseController, that's the kind of controller we want to use
        :param population_count: integer. that's the size of the population, no shit sherlock
        """
        self.population_count = population_count
        self.controller_type = controller_type
        self.population = []
        for _ in range(population_count):
            self.population.append(controller_type([8, 10, 2]))  # This looks pretty scary
        """ Lemme explain that.
        The line above means - construct a list of objects of type controller_type,
        which is population_count long.

        Example?
        let's say we are initiating an EvolutionController object like this:
        my_controller = EvolutionController(DummyController, 10)

        that would make this scary line do the following:
        self.population = 10 * [DummyController()]
        which means a list of 10 DummyControllers.
        We're good now, aren't we?
        """
        self.points = population_count * [0]  # Yup, we also need points for our models

        self.player_1 = 0  # Ready player 1
        self.player_2 = 0

        self.generation = 0
        """
        player_1 and player_2 mean the indexes of models we are putting against each other
        (we can discuss if there's a point in letting a model fight against itself, that's an interesting thought)
        """

    def control_plane(self, which_player, plane_me, plane_enemy, bullets):

        self.population[self.player_1 if which_player == 1 else self.player_2].control(plane_me, plane_enemy, bullets)
        """Yes i am laughing quietly while looking at this line

        if which player = 1, we use self.player_1, otherwise we use self.player_2
        player_1 and player_2 are the indexes of the models.

        So what we're doing here, is we're letting the given plane controller steer our plane
        """

    def score(self, which_player, how_much):
        self.points[self.player_1 if which_player == 1 else self.player_2] += how_much

    def next_pair(self):
        """
        This will switch to the new pair of players.. no idea how to simplify this explanation even more
        :return: there is no return after Bączek told you about machine learning
        """
        self.player_1 += 1
        if self.player_1 == self.population_count:
            self.player_1 = 0
            self.player_2 += 1
            if self.player_2 == self.population_count:
                self.evolve()  # Crooked Colours - Flow is a great song for this kind of work
                self.player_1 = 0
                self.player_2 = 0
                self.generation += 1
                print("reached generation", self.generation)

        print("currently playing:", self.player_1, self.player_2)

    def evolve(self):
        """
        First we will choose the best network by the score,
        Then we copy to replace the whole population list with it,
        Lastly we mutate our new army of neuro-pythonic monsters
        *laughs in tensorflow*
        """
        best_points = max(self.points)
        best_network_index = self.points.index(best_points)  # Index of the network that scored best
        print("the winner is number", best_network_index, "who scored", best_points)
        best_network = self.population[best_network_index]
        for i in range(self.population_count):
            self.population[i] = copy.deepcopy(best_network)
            self.population[i].mutate_by_percent(0.1)  # TODO: make mutation percent differ across the population
