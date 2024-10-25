import math
import pygame

# The Obstacle class represents an in-game object that can
# impede the player in some way
class Obstacle:
    def __init__(self, radius, position, color):
        self.radius = radius
        self.position = position
        self.color = color
        self.is_colliding = False

    def load_sprite(self, sprite):
        pass

    def check_for_player_collision(self, player):
        # Calculate the distance between the player's position and the
        # obstacle's position. If the distance is less than the sum of
        # the radii of the two objects, they are colliding
        dist_x = self.position[0] - player.position[0]
        dist_y = self.position[1] - player.position[1]
        dist_root = math.sqrt((dist_x * dist_x) + (dist_y * dist_y))
        self.is_colliding = dist_root <= (self.radius + player.radius)

    def move(self, dt):
        # In-game obstacles do not move by default
        pass

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)

    def update(self, player, dt):
        if player:
            self.check_for_player_collision(player)

        if not self.is_colliding:
            # If not colliding with the player, the obstacle is free to move
            # provided it is a moving type
            self.move(dt)
