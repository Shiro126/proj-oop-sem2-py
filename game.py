"""
Some smart stuff will be written here some day
"""
from enum import Enum

import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util

import constants
import planes
import controllers
import random
import os
import datetime
import wall


class GameState(Enum):
    running = 0
    plane_1_won = 1
    plane_2_won = 2
    plane_1_crashed = 4
    plane_2_crashed = 5
    collision = 6
    time_over = 7
    quit = 8


# noinspection PyUnusedLocal
class Game:
    def __init__(self):
        """
        Constructor only loads the pygame module,
        then sets the rest of class attributes to None.
        Other tasks such as creating the game window
        are moved to create_basic_game_components method,
        since they will be reused when launching the game
        in different modes (train/vs/whatever else may come)
        """
        # Game engine related
        self.screen = None
        self.clock = None
        self.space = None
        self.draw_options = None
        self.font = None  # But do we really need a font..?

        # Simulation related
        self.bullets = None
        self.game_state = None
        self.plane_1 = None
        self.plane_2 = None
        self.evolution_controller = None
        self.saved_network_filenames = None
        self.game_time = None
        self.fps = constants.FRAMERATE
        self.dt = 1 / self.fps
        self.start_time = None
        self.visible = None

    def create_basic_game_components(self, visible=True):
        """
        Initializes things that are needed to run psychics simulation and graphic engine
        Makes a basic pygame window and connects it with the pymunnk physic engine (if visible set to True)

        :param visible: if visible, you can see what's happening. If not, the simulation runs in turbo mode, invisible
        """

        self.visible = visible
        pygame.init()
        if visible:
            self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)  # connecting the physics to graphics
            self.font = pygame.font.SysFont("Arial", 16)
        else:
            print("running in invisible-turbo-mode")
        self.clock = pygame.time.Clock()
        self.space = pymunk.Space()
        self.space.gravity = 0, constants.GRAVITY_FORCE
        self.game_time = 0.
        current_dir = os.getcwd()
        folder_dir = os.path.join(current_dir, r'saved_networks')
        if not os.path.exists(folder_dir):
            os.makedirs(folder_dir)

        self.start_time = datetime.datetime.now()

    def plane_1_hit_2(self, arbiter, space, data):
        p, b = arbiter.shapes
        if b.body.mass > p.body.mass:
            p, b = b, p
        self.space.remove(b, b.body)
        self.bullets.remove(b.body.parent)
        self.plane_2.plane_hp -= 1
        self.plane_2.bleach()
        self.plane_2.hp_stripe_shapes[self.plane_2.plane_hp].color = pygame.color.THECOLORS["black"]
        if self.plane_2.plane_hp == 0:
            self.game_state = GameState.plane_1_won
        return False

    def plane_2_hit_1(self, arbiter, space, data):
        p, b = arbiter.shapes
        if b.body.mass > p.body.mass:
            p, b = b, p
        self.space.remove(b, b.body)
        self.bullets.remove(b.body.parent)
        self.plane_1.plane_hp -= 1
        self.plane_1.bleach()
        self.plane_1.hp_stripe_shapes[self.plane_1.plane_hp].color = pygame.color.THECOLORS["black"]
        if self.plane_1.plane_hp == 0:
            self.game_state = GameState.plane_2_won
        return False

    def planes_collision(self, arbiter, space, data):
        print("planes collision!")
        self.game_state = GameState.collision
        return False

    def plane_1_wall_collision(self, arbiter, space, data):
        self.game_state = GameState.plane_1_crashed
        print(arbiter.contact_point_set.points)
        return False

    def plane_2_wall_collision(self, arbiter, space, data):
        self.game_state = GameState.plane_2_crashed
        return False

    def initialise_collisions(self):

        plane_a_hit_b_collision = self.space.add_collision_handler(  # Plane a scores
            constants.PLANE_2_COLLISION_TYPE, constants.BULLET_COLLISION_TYPE
        )
        plane_a_hit_b_collision.pre_solve = self.plane_1_hit_2

        plane_b_hit_a_collision = self.space.add_collision_handler(  # Plane b scores
            constants.PLANE_1_COLLISION_TYPE, constants.BULLET_COLLISION_TYPE
        )
        plane_b_hit_a_collision.pre_solve = self.plane_2_hit_1

        planes_collision = self.space.add_collision_handler(  # Smoleńsk
            constants.PLANE_1_COLLISION_TYPE, constants.PLANE_2_COLLISION_TYPE
        )
        planes_collision.pre_solve = self.planes_collision

        plane_1_hit_wall_collision = self.space.add_collision_handler(  # Plane 1 collides with wall
            constants.PLANE_1_COLLISION_TYPE, constants.WALL_COLLISION_TYPE
        )
        plane_1_hit_wall_collision.pre_solve = self.plane_1_wall_collision

        plane_2_hit_wall_collision = self.space.add_collision_handler(  # Plane 2 collides with wall
            constants.PLANE_2_COLLISION_TYPE, constants.WALL_COLLISION_TYPE
        )
        plane_2_hit_wall_collision.pre_solve = self.plane_2_wall_collision

    def simulation_next_step(self):
        """
        This guy does the physics simulation and screen drawing after our game has finished input processing and
        other operations
        """
        if self.visible:
            # Clear screen
            self.screen.fill(pygame.color.THECOLORS["black"])

            # Draw stuff
            self.space.debug_draw(self.draw_options)
            # draw(screen, space)

            pygame.display.flip()
            self.clock.tick(self.fps)

        # Update physics
        self.space.step(self.dt)
        self.game_time += self.dt
        pygame.display.set_caption("Time: " + str(round(self.game_time, 1)))

    def spawn_walls(self):
        """
        Yes, I spawn walls. This is my passion.

        Yes, you need to have a self.space object initialized to spawn walls
        """

        # Vertical walls
        #wall.spawn_wall(constants.SCREEN_HEIGHT, 10, 0, constants.SCREEN_HEIGHT / 2, self.space)
       # wall.spawn_wall(constants.SCREEN_HEIGHT, 10, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT / 2, self.space)

        # Horizontal walls
        #wall.spawn_wall(10, constants.SCREEN_WIDTH, constants.SCREEN_WIDTH / 2, 0, self.space)
        #wall.spawn_wall(10, constants.SCREEN_WIDTH, constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT, self.space)

    def test_vs_dummy(self):
        """
        Fly freely, one dummy plane is spawned to test collisions
        Method used just for testing. SERIOUSLY, USE IT FOR TESTING INSTEAD OF BREAKING OTHER METHODS PLS
        """
        self.create_basic_game_components()
        self.initialise_collisions()  # Collision handling

        # Object spawning
        self.bullets = []
        self.spawn_walls()

        self.plane_1 = planes.spawn_plane(100, 500, self.space, self.bullets, constants.PLANE_1_COLLISION_TYPE)
        human_controller = controllers.HumanController()  # This controller uses keyboard to steer the plane

        # self.plane_2 = planes.spawn_plane(400, 500, self.space, self.bullets, constants.PLANE_2_COLLISION_TYPE)
        # dummy_controller = controllers.DummyController()  # This controller just turns left and shoots all the time

        self.game_state = GameState.running  # This enum will determine whether the game is over and show it's result

        # Here the game starts
        while self.game_state == GameState.running:

            for event in pygame.event.get():  # event loop
                if event.type == QUIT:
                    self.game_state = GameState.quit
            keys = pygame.key.get_pressed()

            human_controller.steer(keys, self.plane_1)
            '''
            Sends the pressed keys into human controller,
            which translates them into plane turning and shooting
            '''

            # dummy_controller.control(self.plane_2, self.plane_1, self.bullets)
            # print(self.plane_2.plane_body.angle)
            '''
            Dummy controller performs his... strategies
            '''

            # if self.is_out_of_map(self.plane_1.plane_body):
            #   self.game_state = GameState.plane_1_crashed

            # if self.is_out_of_map(self.plane_2.plane_body):
            #    self.game_state = GameState.plane_2_crashed

            self.plane_1.update()  # Update the position of both planes,
            # self.plane_2.update()  # according to their angle and speed

            for bullet in self.bullets:  # Update position of each bullet
                bullet.update()

            self.simulation_next_step()  # Draw the simulation

        print("game time:", str(self.game_time), ", game result:", self.game_state)

    @staticmethod
    def get_random_plane_position():
        return random.randrange(1000) + 100, random.randrange(600) + 100

    def load_networks(self):
        """
        This still requires some polishing, the code is not wrong but we need to talk about how the evolution controller
        is constructed (currently it will be deleted in train_visible function, because it is also constructed there,
        so the self.evolution_controller from this function is gone then)
        """
        saved_network_list = os.listdir("saved_networks/")
        # self.evolution_controller = controllers.EvolutionController(controllers.NeuralController, len(network_list))
        for saved_network in saved_network_list:
            print(saved_network_list.index(saved_network), "  ", saved_network)

        chosen_network_indexes_str = input("Enter network numbers")

        chosen_network_indexes_list = chosen_network_indexes_str.split()  # This splits stuff by spaces
        # example: "1 23 6" -> ["1", "23", "6"]
        chosen_network_filenames = []
        chosen_network_indexes_list = list(map(int, chosen_network_indexes_list))
        print(chosen_network_indexes_list[1])

        self.evolution_controller = controllers.EvolutionController(
            controllers.NeuralController,
            len(chosen_network_indexes_list)
        )

        for i in range(len(chosen_network_filenames)):
            self.evolution_controller.population[i].load_from_json(chosen_network_filenames[i])
        # print(self.evolution_controller.population[1].weights)

    def train_visible(self):
        """
        Trains the network and lets the user see
        the progress made by the network.
        Simulation runs in real-time
        """

        self.create_basic_game_components(visible=True)
        self.initialise_collisions()  # Collision handling

        # Object spawning
        self.bullets = []

        self.plane_1 = planes.spawn_plane(100, 500, self.space, self.bullets, constants.PLANE_1_COLLISION_TYPE)
        self.plane_2 = planes.spawn_plane(400, 500, self.space, self.bullets, constants.PLANE_2_COLLISION_TYPE)
        self.plane_1.plane_body.position = (300, 500)
        self.plane_2.plane_body.position = (700, 500)
        self.plane_2.plane_body.angle = 3.14
        self.plane_1.speed = constants.PLANE_STARTING_SPEED
        self.plane_2.speed = constants.PLANE_STARTING_SPEED

        evolution_controller = controllers.EvolutionController(controllers.NeuralController, 5)

        self.game_state = GameState.running  # This enum will determine whether the game is over and show it's result
        while self.game_state != GameState.quit:
            # Here the game starts
            while self.game_state == GameState.running:

                for event in pygame.event.get():  # event loop
                    if event.type == QUIT:
                        self.game_state = GameState.quit
                keys = pygame.key.get_pressed()

                if keys[K_s]:
                    filename = input("Enter filename")
                    evolution_controller.population[evolution_controller.player_1].save_to_json(filename)

                if self.game_time > 20:
                    self.game_state = GameState.time_over

                self.plane_1.update()  # Update the position of both planes,
                self.plane_2.update()  # according to their angle and speed

                for bullet in self.bullets:  # Update position of each bullet
                    bullet.update()

                self.simulation_next_step()  # Draw the simulation

            print("game time:", str(self.game_time), ", game result:", self.game_state)
            if self.game_state == GameState.quit:
                continue

            # Give scores
            if self.game_state == GameState.plane_1_won:
                evolution_controller.score(1, self.game_time + 30)
                evolution_controller.score(2, self.game_time * 0.5)

            elif self.game_state == GameState.plane_2_won:
                evolution_controller.score(2, self.game_time + 30)
                evolution_controller.score(1, self.game_time * 0.5)

            elif self.game_state == GameState.plane_1_crashed:
                evolution_controller.score(2, self.game_time)

            elif self.game_state == GameState.plane_2_crashed:
                evolution_controller.score(1, self.game_time)

            elif self.game_state == GameState.time_over:
                evolution_controller.score(2, 10)
                evolution_controller.score(1, 10)

            evolution_controller.score(1, self.plane_1.plane_hp)
            evolution_controller.score(2, self.plane_2.plane_hp)

            evolution_controller.next_pair()
            self.plane_1.plane_body.position = (300, 500)
            self.plane_2.plane_body.position = (700, 500)
            self.plane_2.plane_body.angle = 3.14
            self.game_state = GameState.running
            self.plane_1.plane_hp = constants.PLANE_HP
            self.plane_2.plane_hp = constants.PLANE_HP
            self.game_time = 0.
            self.plane_1.reset()
            self.plane_2.reset()
            self.plane_1.speed = constants.PLANE_STARTING_SPEED
            self.plane_2.speed = constants.PLANE_STARTING_SPEED


if __name__ == "__main__":
    my_game = Game()
    # my_game.load_networks()
    my_game.test_vs_dummy()
    """"
    game_options = {}
    game_options['1'] = "Test vs dummy"
    game_options['2'] = "Train visible (from the start)"
    game_options['3'] = "Train visible (load a network from file)"
    game_options['4'] = "Show saved networks"
    game_options['5'] = "Play with a saved network"

    while True:
        keys = sorted(game_options)
        for key in keys:
            print (key, game_options[key])
        selection = input("Select: ")
        if selection == '1':
            my_game.test_vs_dummy()
        if selection == '2':
            my_game.train_visible()
        if selection == '3':
            
    """
