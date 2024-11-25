import pygame
import math
import random
from projectiles.enemy_projectile import EnemyProjectile
from projectiles.enemy_projectile_angled import EnemyProjectileAngled

class Boss(pygame.sprite.DirtySprite):
    def __init__(self, x, y, current_time, difficulty):
        super().__init__()
        self.difficulty = difficulty
        self.max_health = 100 + (15 * difficulty)
        self.health = 1 #self.max_health SET TO 1 FOR TESTING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.living = True
        self.time_destroyed = 0
        self.color = (255, 0, 0) # Default red color, will change when we have sprites
        self.spawn_destination_y = y
        self.size = 100 # Used for destruction explosion
        self.velocity = 1
        self.heading_home = False
        self.fire_delay = 1.1  # Time between shots
        self.switch_delay = 5
        self.last_shot_time = current_time
        self.prev_shot_type = 3
        self.curr_shot_type = 0
        self.last_switch_time = current_time
        self.spread_type = 0 # Used for spread shot logic
        self.angled_shot_speed = 3
        self.at_y_level = False
        
        self.centerSize = 75
        self.wingSizeX = 75
        self.wingSizeY = 20
        
        width = self.centerSize + 2 * self.wingSizeX  # Total width
        height = self.centerSize # Total height
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.drawShip()
        
        # Positioning box
        self.rect = self.image.get_rect(center=(x, -500))
        # Hit boxes
        self.central_rect = pygame.Rect(
            self.rect.x + self.wingSizeX,
            self.rect.y + (self.rect.height - self.centerSize) // 2,
            self.centerSize,
            self.centerSize
        )
        self.left_wing_rect = pygame.Rect(
            self.rect.x,
            self.rect.y + (self.rect.height - self.wingSizeY) // 2,
            self.wingSizeX,
            self.wingSizeY
        )
        self.right_wing_rect = pygame.Rect(
            self.rect.x + self.wingSizeX + self.centerSize,
            self.rect.y + (self.rect.height - self.wingSizeY) // 2,
            self.wingSizeX,
            self.wingSizeY
        )        
    
    def drawShip(self): # Determines shape and color of ship
        # Clear the surface with transparency
        self.image.fill((0, 0, 0, 0))  # Fill with transparent color
        # Central square
        square_rect = pygame.Rect(
            self.wingSizeX,  # Positioned in the center horizontally
            (self.image.get_height() - self.centerSize) // 2,  # Vertically centered
            self.centerSize,
            self.centerSize
        )
        pygame.draw.rect(self.image, self.color, square_rect)
        # Left wing
        left_rect = pygame.Rect(
            0,  # Start at the far left
            (self.image.get_height() - self.wingSizeY) // 2,  # Vertically centered
            self.wingSizeX,
            self.wingSizeY
        )
        pygame.draw.rect(self.image, self.color, left_rect)
        # Right wing
        right_rect = pygame.Rect(
            self.centerSize + self.wingSizeX,  # Positioned next to the square
            (self.image.get_height() - self.wingSizeY) // 2,  # Vertically centered
            self.wingSizeX,
            self.wingSizeY
        )
        pygame.draw.rect(self.image, self.color, right_rect)
           
    def fire_shot(self, proj_group, paused, curr, player_pos_x, player_pos_y):
        current_time = curr
        if (self.living == True and paused == False and self.at_y_level == True):
            # Directed shots
            if (self.curr_shot_type == 0):
                self.angled_shot_speed = 5
                self.fire_delay = .25 - (.05 * self.difficulty)
                curr_angle = math.degrees(math.atan2(player_pos_y - self.rect.centery, player_pos_x - self.rect.centerx))
                if (current_time - self.last_shot_time >= self.fire_delay):
                    projectile = EnemyProjectileAngled(self.rect.centerx, self.rect.centery, curr_angle, self.angled_shot_speed)
                    proj_group.add(projectile)
                    self.last_shot_time = current_time
                # Switch
                if (current_time - self.switch_delay >= self.last_switch_time):
                    self.last_switch_time = current_time
                    self.prev_shot_type = self.curr_shot_type
                    self.curr_shot_type = random.randint(1, 2)
            # Dual spreads
            elif (self.curr_shot_type == 1):
                self.angled_shot_speed = 3
                self.fire_delay = .7 - (.15 * self.difficulty)
                if (current_time - self.last_shot_time >= self.fire_delay):
                    if(self.spread_type == 0):
                        projectile = EnemyProjectile(self.rect.centerx, self.rect.centery, self.angled_shot_speed)
                        angled_projectile_a = EnemyProjectileAngled(self.rect.centerx, self.rect.centery, 135, self.angled_shot_speed)
                        angled_projectile_b = EnemyProjectileAngled(self.rect.centerx, self.rect.centery, 45, self.angled_shot_speed)
                        proj_group.add(projectile)
                        proj_group.add(angled_projectile_a)
                        proj_group.add(angled_projectile_b)
                        self.spread_type = 1
                    else:
                        angled_projectile_a = EnemyProjectileAngled(self.rect.centerx, self.rect.centery, 20, self.angled_shot_speed)
                        angled_projectile_b = EnemyProjectileAngled(self.rect.centerx, self.rect.centery, 70, self.angled_shot_speed)
                        angled_projectile_c = EnemyProjectileAngled(self.rect.centerx, self.rect.centery, 110, self.angled_shot_speed)
                        angled_projectile_d = EnemyProjectileAngled(self.rect.centerx, self.rect.centery, 160, self.angled_shot_speed)
                        proj_group.add(angled_projectile_a)
                        proj_group.add(angled_projectile_b)
                        proj_group.add(angled_projectile_c)
                        proj_group.add(angled_projectile_d)
                        self.spread_type = 0
                    self.last_shot_time = current_time
                # Switch
                if (current_time - self.switch_delay >= self.last_switch_time):
                    self.last_switch_time = current_time
                    tempPrevShot = self.prev_shot_type
                    self.prev_shot_type = self.curr_shot_type
                    if(tempPrevShot == 0):
                        self.curr_shot_type = 2
                    elif(tempPrevShot == 2):
                        self.curr_shot_type = 0
            # Bullet rain from wings
            elif (self.curr_shot_type == 2):
                self.fire_delay = .2 - (.05 * self.difficulty)
                if (current_time - self.last_shot_time >= self.fire_delay):
                    projectile = EnemyProjectile(self.rect.centerx + 90, self.rect.centery, 4)
                    proj_group.add(projectile)
                    projectile = EnemyProjectile(self.rect.centerx - 90, self.rect.centery, 4)
                    proj_group.add(projectile)
                    self.last_shot_time = current_time
                # Switch    
                if (current_time - self.switch_delay >= self.last_switch_time):
                    self.last_switch_time = current_time
                    self.prev_shot_type = self.curr_shot_type
                    self.curr_shot_type = random.randint(0, 1)
            
    def decrease_health(self, damage = 1):
        self.health -= damage
        if(self.health < 1):
            self.living = False
            self.time_destroyed = pygame.time.get_ticks()
            
    def change_color(self):
        if(self.health == self.max_health / 2):
            self.color = (255,100,0)
            self.drawShip()
        if(self.health == self.max_health / 5):
            self.color = (255,140,0)
            self.drawShip()
    
    def update(self, paused, curr_time): # Updates position, will move left and right between specific values, and moves down upon spawning
        if (self.rect.centery < self.spawn_destination_y and paused == False):
            self.rect.y += self.velocity 
            self.rect.centery += self.velocity
            self.central_rect.y = self.rect.y + (self.rect.height - self.wingSizeY) // 2
            self.left_wing_rect.y = self.rect.y + (self.rect.height - self.wingSizeY) // 2
            self.right_wing_rect.y = self.rect.y + (self.rect.height - self.wingSizeY) // 2
            if(self.rect.centery >= self.spawn_destination_y):
                self.at_y_level = True
                self.velocity = 2
                self.last_switch_time = curr_time
        elif (self.living == True and paused == False):
            if (self.rect.centerx >= 600 or self.rect.centerx <= 200):
                self.velocity *= -1
            self.rect.x += self.velocity
            
            self.central_rect.x = self.rect.x + self.wingSizeX
            self.left_wing_rect.x = self.rect.x
            self.right_wing_rect.x = self.rect.x + self.wingSizeX + self.centerSize