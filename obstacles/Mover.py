import math
from obstacles.Obstacle import Obstacle

# The Mover class represents an Obstacle that moves in
# a straight line along the screen
class Mover(Obstacle):
    def __init__(self, position, velocity, sprite_path):
        super().__init__(position, sprite_path)

        self.velocity = velocity
        self.color = (100, 100, 100)

    def adjust_velocity(self, x, y):
        self.velocity = (self.velocity[0] + x, self.velocity[1] + y)

    def move(self, dt):
        new_x_pos = self.position[0] + math.ceil(self.velocity[0] * dt)
        new_y_pos = self.position[1] + math.ceil(self.velocity[1] * dt)
        self.position = (new_x_pos, new_y_pos)
