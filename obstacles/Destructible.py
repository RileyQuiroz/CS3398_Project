import pygame
from obstacles.Obstacle import Obstacle

# The Destructible class represents an Obstacle that
# can be destroyed by the player
class Destructible(Obstacle):
    def __init__(self, position, health, score_system, scale, sprite_path):
        super().__init__(position, scale, sprite_path)

        self.max_health = health
        self.health = self.max_health
        self.score_system = score_system
        self.destroyed = False
        self.color = (175, 175, 175)
        self.health_bar = pygame.rect.Rect(self.rect.x, self.rect.y - 5, self.rect.width, 3)

    def draw(self, surface):
        if not self.destroyed:
            super().draw(surface)
            pygame.draw.rect(surface, (100, 255, 100), self.health_bar)

    def take_damage(self):
        self.health -= 1

        if self.health <= 0:
            self.destroyed = True
            self.score_system.increase_flat(20)

    def update(self, player, dt):
        if not self.destroyed:
            super().update(player, dt)

            self.health_bar.x = self.rect.x
            self.health_bar.y = self.rect.y - 5

            for bullet in player.projectiles_group:
                if pygame.sprite.collide_rect(self, bullet):
                    self.take_damage()
                    bullet.kill()
                    self.health_bar.width = self.rect.width / self.max_health * self.health
