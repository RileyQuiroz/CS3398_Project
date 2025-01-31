import pygame
import math
from characters.enemies.enemy_structure import Enemy
from projectiles.enemy_projectile import EnemyProjectile
from projectiles.enemy_projectile_angled import EnemyProjectileAngled

class EnemyTypeB(Enemy):
    def __init__(self, x, y, left_bound, right_bound, current_time):
        super().__init__(3, x, y)
        self.size = 25  
        self.velocity = 4
        self.left_bound = left_bound
        self.right_bound = right_bound  

        image = pygame.image.load("assets/enemies/enemy_type_b.png").convert_alpha()
        self.image = pygame.transform.scale_by(image, (2, 2))

        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        self.fire_delay = 1.4  # Time between shots
        self.last_shot_time = current_time  # Time since the last shot
        self.movement_angle = 0
        self.movement_radius = right_bound - x
        self.movement_direction = 0.05
        self.movement_center = x
        self.movement_stop_time = 0
        self.arc_stopped = False
        self.arcs_complete = 0
        
    def fire_shot(self, proj_group, paused, curr, empty1, empty2): # Fires a spread of bullets
        current_time = curr
        # Check if enough time has passed since the last shot
        if (current_time - self.last_shot_time >= self.fire_delay and self.living == True and paused == False and self.heading_home == False):
            projectile = EnemyProjectile(self.rect.centerx, self.rect.centery, 5)
            angled_projectile_a = EnemyProjectileAngled(self.rect.centerx, self.rect.centery, 135, 5)
            angled_projectile_b = EnemyProjectileAngled(self.rect.centerx, self.rect.centery, 45, 5)
            # Shotgun type attack
            proj_group.add(projectile)
            proj_group.add(angled_projectile_a)
            proj_group.add(angled_projectile_b)
            self.last_shot_time = current_time
    
    
    def update(self, paused, curr_time): # Updates position, will move left and right between specific values, and moves down upon spawning
        # Move into position
        if(self.pos_x < self.right_bound+20 and self.heading_home == False and paused == False):
            self.rect.x += self.velocity 
            self.pos_x += self.velocity
        elif (self.pos_y < self.spawn_destination_y and self.heading_home == False and paused == False):
            self.rect.y += self.velocity 
            self.pos_y += self.velocity
        # Go home
        elif (self.heading_home == True and self.living == True and paused == False):
            self.rect.y -= 2 
            self.pos_y -= 2
        # Movement
        elif (self.living == True and paused == False):
            if(self.arc_stopped == False):
                self.movement_angle += self.movement_direction
            if (self.movement_angle >= math.pi or self.movement_angle <= 0):  # math.pi radians = 180 degrees
                if(self.arc_stopped == False): # Stops when at either end of arc
                    self.movement_stop_time = curr_time
                    self.arc_stopped = True
                    self.arcs_complete += 1
                    if(self.arcs_complete == 5): # Leave after 5 arcs completed
                        self.heading_home = True
                elif(curr_time - self.movement_stop_time >= 2): # Moves every two seconds
                    self.arc_stopped = False
                    self.movement_direction = -1 * self.movement_direction
            # Update position along the circular arc
            if(self.arc_stopped == False):
                self.rect.x = self.movement_center + int(self.movement_radius * math.cos(self.movement_angle))
                self.rect.y = self.pos_y + int(self.movement_radius * math.sin(self.movement_angle))