import constants
import pymunk  # For constructing the plane body
import custom_objects


def spawn_wall(height, width, position_x, position_y, space):
    wall = Wall(height, width, position_x, position_y)
    space.add(wall.wall_body, wall.wall_shape)


class Wall:
    def __init__(self, height, width, position_x, position_y):
        self.wall_body = custom_objects.BetterBody(
            constants.WALL_MASS,
            constants.WALL_INERTIA,
            pymunk.Body.STATIC,
            self
        )

        self.wall_body.position = position_x, position_y
        self.wall_shape = pymunk.Poly.create_box(self.wall_body, size=(width, height))
        self.wall_shape.collision_type = constants.WALL_COLLISION_TYPE
