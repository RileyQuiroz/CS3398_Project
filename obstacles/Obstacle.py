from math import sqrt
import pygame

# The Obstacle class represents an in-game object that can
# impede the player in some way.
class Obstacle:
    def __init__(self, radius, position, color):
        self.radius = radius
        self.position = position
        self.velocity = (0, 0)
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
        dist_root = sqrt((dist_x * dist_x) + (dist_y * dist_y))
        self.is_colliding = dist_root <= (self.radius + player.radius)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)

    def update(self, player, dt):
        self.check_for_player_collision(player)

        if not self.is_colliding:
            # If not colliding with the player, the obstacle is free to move
            new_x_pos = self.position[0] + (self.velocity[0] * dt)
            new_y_pos = self.position[1] + (self.velocity[1] * dt)
            self.position = (new_x_pos, new_y_pos)
