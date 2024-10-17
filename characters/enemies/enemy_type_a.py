import pygame
from characters.enemies.enemy_structure import Enemy

class EnemyTypeA(Enemy):
    def __init__(self, x, y):
        super().__init__(3, 0, x, y)
        self.size = 25  
        self.velocity = 4  
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))