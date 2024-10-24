import math
from obstacles.Obstacle import Obstacle

class Mover(Obstacle):
    def __init__(self, radius, position, velocity, color):
        super().__init__(radius, position, color)

        self.velocity = velocity

    def adjust_velocity(self, x, y):
        self.velocity = (self.velocity[0] + x, self.velocity[1] + y)

    def move(self, dt):
        new_x_pos = self.position[0] + math.ceil(self.velocity[0] * dt)
        new_y_pos = self.position[1] + math.ceil(self.velocity[1] * dt)
        self.position = (new_x_pos, new_y_pos)
