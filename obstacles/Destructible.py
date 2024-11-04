import pygame
from obstacles.Obstacle import Obstacle

# The Destructible class represents an Obstacle that
# can be destroyed by the player
class Destructible(Obstacle):
    def __init__(self, position, health, sprite_path):
        super().__init__(position, sprite_path)

        self.health = health
        self.destroyed = False

    def draw(self, surface):
        if not self.destroyed:
            super().draw(surface)

    def take_damage(self):
        self.health -= 1

        if self.health <= 0:
            self.destroyed = True

    def update(self, player, dt):
        if not self.destroyed:
            super().update(player, dt)

            for bullet in player.projectiles_group:
                if pygame.sprite.collide_rect(self, bullet):
                    self.take_damage()
                    bullet.kill()


