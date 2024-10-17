import pygame
from characters.enemies.enemy_structure import Enemy
from characters.enemies.enemy_projectile import EnemyProjectile

class EnemyTypeA(Enemy):
    def __init__(self, x, y, left_bound, right_bound):
        super().__init__(3, 0, x, y)
        self.size = 25  
        self.velocity = 3
        self.left_bound = left_bound
        self.right_bound = right_bound  
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        self.fire_delay = 800  # Time between shots (in milliseconds)
        self.last_shot_time = pygame.time.get_ticks()  # Time since the last shot
        
    def fire_shot(self, proj_group): # Fires a single bullet
        current_time = pygame.time.get_ticks()
        # Check if enough time has passed since the last shot
        if current_time - self.last_shot_time >= self.fire_delay:
            projectile = EnemyProjectile(self.rect.centerx, self.rect.centery)
            proj_group.add(projectile)
            self.last_shot_time = current_time
    
    def update(self): # Updates position, will move left and right between specific values
        if self.rect.centerx >= self.right_bound or self.rect.centerx <= self.left_bound:
            self.velocity *= -1
        self.rect.x += self.velocity