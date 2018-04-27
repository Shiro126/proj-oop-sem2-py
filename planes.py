import constants
from pygame.locals import *  # Keys
import pygame
import pymunk  # For constructing the plane body
from pymunk.vec2d import Vec2d  # Vector calculations - needed for the plane to fly like a goddamn plane does
import math  # Żeby Pan Merdas był wesoły <3
from enum import Enum
import bullet


class DIRECTION(Enum):
    LEFT = 1.
    RIGHT = -1


def spawn_plane(position_x, position_y, space, bullets, collision_type):
    """
    A helper function that will create plane objects and spawn them into the game space
    :param position_x: spawn x position
    :param position_y: spawn y position
    :param space: the pymunk space to spawn our plane
    :param bullets: reference to bullets array
    :param collision_type: plane's collision type
    :returns a plane object that was created
    """
    plane = Plane(position_x, position_y, space, bullets, collision_type)
    space.add(plane.plane_body, plane.plane_shape)
    for i in range(len(plane.hp_stripe_shapes)):
        space.add(plane.hp_stripe_shapes[i])

    return plane


class Plane:

    def __init__(self, start_x, start_y, space, bullets, collision_type):
        self.plane_body = pymunk.Body(constants.PLANE_MASS,
                                      constants.PLANE_INERTIA, body_type=pymunk.Body.DYNAMIC)
        self.plane_body.center_of_gravity = constants.PLANE_GRAVITY_CENTER
        self.plane_body.position = start_x, start_y
        self.plane_shape = pymunk.Poly(self.plane_body, constants.PLANE_VERTICES)
        self.plane_shape.color = pygame.color.THECOLORS["red"]
        self.plane_shape.collision_type = collision_type
        self.plane_body.angle = 0  # works, no idea why
        self.hp_stripe_bodies = []
        self.hp_stripe_shapes = []

        for i in range(constants.PLANE_HP):
            self.hp_stripe_bodies.append(pymunk.Body(body_type=pymunk.Body.KINEMATIC))
            self.hp_stripe_shapes.append(pymunk.Poly(self.hp_stripe_bodies[i], constants.HP_STRIPE_VERTICES))
            self.hp_stripe_bodies[i].position = (start_x + i*5)-8, start_y + 30
            self.hp_stripe_bodies[i].angle = 0  # let's leave it like that
            self.hp_stripe_shapes[i].color = pygame.color.THECOLORS["green"]

        self.speed = constants.PLANE_STARTING_SPEED
        self.space = space
        self.bullets = bullets
        self.ammo = constants.PLANE_STARTING_AMMO
        self.can_shoot = True
        self.plane_hp = constants.PLANE_HP

    def reset(self):
        self.plane_shape.color = pygame.color.THECOLORS["red"]
        for i in range(constants.PLANE_HP):
            self.hp_stripe_shapes[i].color = pygame.color.THECOLORS["green"]

    def update(self):  # Called every frame
        # Engine
        self.speed -= math.sin(self.plane_body.angle) * constants.PLANE_SPEED_CHANGE_RATE
        if self.speed < constants.PLANE_MIN_SPEED:
            self.speed = constants.PLANE_MIN_SPEED
        elif self.speed > constants.PLANE_MAX_SPEED:
            self.speed = constants.PLANE_MAX_SPEED
        self.plane_body.position += Vec2d(self.speed, 0).rotated(self.plane_body.angle)
        if self.plane_body.position[0]>1210:
            self.plane_body.position-=Vec2d(1220,0)
        if self.plane_body.position[1]>810:
            self.plane_body.position-=Vec2d(0,820)
        if self.plane_body.position[0]<-10:
            self.plane_body.position+=Vec2d(1220,0)
        if self.plane_body.position[1]<-10:
            self.plane_body.position+=Vec2d(0,820)    
        for i in range(len(self.hp_stripe_bodies)):
            self.hp_stripe_bodies[i].position = (self.plane_body.position[0] + i*5 - 8, self.plane_body.position[1] + 30)
        if self.ammo < constants.PLANE_STARTING_AMMO:
            self.ammo += 0.1
        else:
            self.can_shoot = True
        # print(self.ammo)

    def turn(self, direction):
        self.plane_body.angle += direction.value * constants.PLANE_ROTATION_SPEED * self.speed
        if self.plane_body.angle > 6.28318531:      # I am aware
            self.plane_body.angle -= 6.28318531     # That this thing
        elif self.plane_body.angle < -6.28318531:   # looks
            self.plane_body.angle += 6.28318531     # fucking terrible

    def shoot(self):
        if self.ammo > 0 and self.can_shoot:
            bullet.spawn_bullet(
                self.space,
                self.plane_body.position,
                self.plane_body.angle,
                self.bullets,
                self.plane_shape.collision_type
            )
            self.ammo -= 1
        else:
            self.can_shoot = False

    def bleach(self):
        try:
            l = list(self.plane_shape.color)
            l[0] += (255 - l[0]) / (self.plane_hp + 1)
            l[1] += (255 - l[1]) / (self.plane_hp + 1)
            l[2] += (255 - l[2]) / (self.plane_hp + 1)
            self.plane_shape.color = tuple(l)
        except ZeroDivisionError:
            return

