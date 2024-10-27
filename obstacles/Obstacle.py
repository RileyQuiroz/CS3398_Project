import math
import pygame

# The Obstacle class represents an in-game object that can
# impede the player in some way
class Obstacle:
    def __init__(self, position, sprite_path):
        self.position = position
        self.sprite = pygame.image.load(sprite_path).convert_alpha()
        self.is_colliding = False

    def check_for_player_collision(self, player):
        # Check for collision by comparing bitmaps
        self.is_colliding = pygame.sprite.collide_mask(self.sprite, player.sprite)

    def move(self, dt):
        # In-game obstacles do not move by default
        pass

    def draw(self, surface):
        surface.blit(self.sprite, self.position)

    def update(self, player, dt):
        if player:
            self.check_for_player_collision(player)

        if not self.is_colliding:
            # If not colliding with the player, the obstacle is free to move
            # provided it is a moving type
            self.move(dt)
