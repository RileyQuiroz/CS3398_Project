import math
from obstacles.Mover import Mover
from obstacles.Rotator import Rotator

# The ZigZag class represents an Obstacle that moves
# in a zig-zag pattern along a specified trajectory
class ZigZag(Mover, Rotator):
    def __init__(self, position, velocity, sprite_path):
        Rotator.__init__(self, position, sprite_path)
        Mover.__init__(self, position, velocity, sprite_path)
    
    def move(self, dt):
        self.rotate(dt)

        new_x_pos = self.position[0] + math.ceil(self.velocity[0] * dt)
        new_y_pos = self.position[1] + math.ceil(self.velocity[1] * dt) + math.sin(self.theta) * 3

        self.position = (new_x_pos, new_y_pos)
