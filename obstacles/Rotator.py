import math
from obstacles.Obstacle import Obstacle

# The Rotator class represents an Obstacles that moves
# in a circle around a central point in the game
# environment
class Rotator(Obstacle):
    def __init__(self, radius, position, color):
        super().__init__(radius, position, color)

        self.center = self.position
        self.theta = 0
        self.rotational_speed = 2
        self.center_distance = 100

    def rotate(self, dt):
        self.theta = self.theta + self.rotational_speed * dt

        # If the obstacle has completed a rotation, the angle
        # resets back to 0
        if self.theta >= math.pi * 2:
            self.theta = self.theta - math.pi * 2

    def move(self, dt):
        self.rotate(dt)

        new_x_pos = self.center[0] + math.cos(self.theta) * self.center_distance
        new_y_pos = self.center[1] + math.sin(self.theta) * self.center_distance

        self.position = (new_x_pos, new_y_pos)
