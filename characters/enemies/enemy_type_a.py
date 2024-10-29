import pygame
from characters.enemies.enemy_structure import Enemy
from characters.enemies.enemy_projectile import EnemyProjectile

class EnemyTypeA(Enemy):
    def __init__(self, x, y, left_bound, right_bound, current_time):
        super().__init__(3, x, y)
        self.size = 25  
        self.velocity = 3
        self.left_bound = left_bound
        self.right_bound = right_bound  
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        self.fire_delay = 0.9  # Time between shots
        self.last_shot_time = current_time  # Time since the last shot
        
    def fire_shot(self, proj_group, paused, curr): # Fires a single bullet
        current_time = curr
        # Check if enough time has passed since the last shot
        if (current_time - self.last_shot_time >= self.fire_delay and self.living == True and paused == False):
            projectile = EnemyProjectile(self.rect.centerx, self.rect.centery)
            proj_group.add(projectile)
            self.last_shot_time = current_time
    
    def update(self, paused): # Updates position, will move left and right between specific values, and moves down upon spawning
        if (self.pos_y < self.spawn_destination_y and paused == False):
            self.rect.y += self.velocity 
            self.pos_y += self.velocity
        elif (self.living == True and paused == False):
            if (self.rect.centerx >= self.right_bound or self.rect.centerx <= self.left_bound):
                self.velocity *= -1
            self.rect.x += self.velocity