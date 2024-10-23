from obstacles.Obstacle import Obstacle
import math

class Rotator(Obstacle):
    def __init__(self, radius, position, velocity, color):
        super().__init__(radius, position, velocity, color)

        self.center = self.position
        self.theta = 0
        self.rotational_speed = 2
        self.center_distance = 200

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
