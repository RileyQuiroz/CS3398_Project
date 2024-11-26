import pygame
from characters.enemies.enemy_structure import Enemy
from projectiles.enemy_projectile_delbur import EnemyProjectileDelayBurst

class EnemyTypeC(Enemy):
    def __init__(self, x, y, left_bound, right_bound, current_time):
        super().__init__(6, x, y)
        self.size = 32  
        self.velocity = 1
        self.left_bound = left_bound
        self.right_bound = right_bound  

        image = pygame.image.load("assets/enemies/enemy_type_c.png").convert_alpha()
        self.image = pygame.transform.scale_by(image, (2.5, 2.5))

        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        self.fire_delay = 2.5  # Time between shots
        self.last_shot_time = current_time  # Time since the last shot
        
    def fire_shot(self, proj_group, paused, curr, empty1, empty2): # Fires a single bullet
        current_time = curr
        # Check if enough time has passed since the last shot
        if (current_time - self.last_shot_time >= self.fire_delay and self.living == True and paused == False and self.heading_home == False):
            projectile = EnemyProjectileDelayBurst(self.rect.centerx, self.rect.centery, 2, current_time)
            proj_group.add(projectile)
            self.last_shot_time = current_time
    
    def update(self, paused, curr_time): # Updates position, will move left and right between specific values, and moves down upon spawning
        if (self.pos_y < self.spawn_destination_y and self.heading_home == False and paused == False):
            self.rect.y += self.velocity 
            self.pos_y += self.velocity
        elif (self.living == True and paused == False):
            if (self.rect.centerx >= self.right_bound or self.rect.centerx <= self.left_bound):
                self.velocity *= -1
            self.rect.x += self.velocity