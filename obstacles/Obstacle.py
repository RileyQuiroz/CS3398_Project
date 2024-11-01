import math
import pygame

# The Obstacle class represents an in-game object that can
# impede the player in some way
class Obstacle:
    def __init__(self, position, sprite_path):
        self.position = position
        self.velocity = (0, 0)
        self.sprite = pygame.image.load(sprite_path).convert_alpha()
        self.rect = pygame.Rect(self.position[0], self.position[1], 60, 60)
        self.is_colliding = False

    def check_for_player_collision(self, player):
        # Check for collision by comparing bitmaps
        self.is_colliding = pygame.sprite.collide_rect(self, player)

    def handle_player_collision(self, player):
        center = (self.position[0] + self.rect.width / 2, self.position[1] + self.rect.height / 2)
        playerCenter = (player.x + player.rect.width / 2, player.y + player.rect.height / 2)
        x_dist = playerCenter[0] - center[0]
        y_dist = playerCenter[1] - center[1]


        if x_dist < 0:
            x_dir = -1
        else:
            x_dir = 1

        if y_dist < 0:
            y_dir = -1
        else:
            y_dir = 1

        player.x += self.velocity[0] * x_dir
        player.y += self.velocity[1] * y_dir

    def move(self, dt):
        # In-game obstacles do not move by default
        pass

    def draw(self, surface):
        # surface.blit(self.sprite, self.position)
        pygame.draw.rect(surface, (100, 100, 100), self.rect)

    def update(self, player, dt):
        if player:
            self.check_for_player_collision(player)

        if self.is_colliding:
            self.handle_player_collision(player)
        else:
            # If not colliding with the player, the obstacle is free to move
            # provided it is a moving type
            self.move(dt)

        self.rect.x = self.position[0]
        self.rect.y = self.position[1]