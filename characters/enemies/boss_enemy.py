import pygame
import random
from projectiles.enemy_projectile import EnemyProjectile

class Boss(pygame.sprite.DirtySprite):
    def __init__(self, x, y, current_time):
        super().__init__()
        self.max_health = 100
        self.health = 100
        self.living = True
        self.time_destroyed = 0
        self.color = (255, 0, 0) # Default red color, will change when we have sprites
        self.spawn_destination_y = y
        self.size = 100 # Used for destruction explosion
        self.velocity = 2
        self.heading_home = False
        self.fire_delay = 1.1  # Time between shots
        self.switch_delay = 5
        self.last_shot_time = current_time
        self.prev_shot_type = 0
        self.curr_shot_type = 2
        self.last_switch_time = current_time
        self.spread_type = 0 # Used for spread shot logic
        
        self.centerSize = 75
        self.wingSizeX = 75
        self.wingSizeY = 20
        
        width = self.centerSize + 2 * self.wingSizeX  # Total width
        height = self.centerSize # Total height
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.drawShip()
        
        # Positioning box
        self.rect = self.image.get_rect(center=(x, y))
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
           
    def fire_shot(self, proj_group, paused, curr): # Will have three firing modes
        current_time = curr
        if (self.living == True and paused == False and self.heading_home == False):
            # Directed shots
            if (self.curr_shot_type == 0):
                self.fire_delay = 1.1
                if (current_time - self.last_shot_time >= self.fire_delay):
                    projectile = EnemyProjectile(self.rect.centerx, self.rect.centery)
                    proj_group.add(projectile)
                    self.last_shot_time = current_time
                if (current_time - self.switch_delay >= self.last_switch_time):
                    # Switch
                    self.last_switch_time = current_time
                    self.prev_shot_type = self.curr_shot_type
                    self.curr_shot_type = random.randint(0, 2)
                    print(self.curr_shot_type)
            # Dual spreads
            elif (self.curr_shot_type == 1):
                self.fire_delay = 1.1
                if (current_time - self.last_shot_time >= self.fire_delay):
                    projectile = EnemyProjectile(self.rect.centerx, self.rect.centery)
                    proj_group.add(projectile)
                    self.last_shot_time = current_time
                    # Switch
                if (current_time - self.switch_delay >= self.last_switch_time):
                    self.last_switch_time = current_time
                    self.prev_shot_type = self.curr_shot_type
                    self.curr_shot_type = random.randint(0, 1)
                    if(self.curr_shot_type == 1):
                        self.curr_shot_type == 2
                    print(self.curr_shot_type)
            # Bullet rain from wings
            elif (self.curr_shot_type == 2):
                self.fire_delay = .3
                if (current_time - self.last_shot_time >= self.fire_delay):
                    projectile = EnemyProjectile(self.rect.centerx + 90, self.rect.centery)
                    proj_group.add(projectile)
                    projectile = EnemyProjectile(self.rect.centerx - 90, self.rect.centery)
                    proj_group.add(projectile)
                    self.last_shot_time = current_time
                # Switch    
                if (current_time - self.switch_delay >= self.last_switch_time):
                    self.last_switch_time = current_time
                    self.prev_shot_type = self.curr_shot_type
                    self.curr_shot_type = random.randint(0, 1)
                    print(self.curr_shot_type)
            
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
        if (self.rect.centery < self.spawn_destination_y and self.heading_home == False and paused == False):
            self.rect.y += self.velocity 
            self.rect.centery += self.velocity
        elif (self.living == True and paused == False):
            if (self.rect.centerx >= 600 or self.rect.centerx <= 200):
                self.velocity *= -1
            self.rect.x += self.velocity
            
            self.central_rect.x = self.rect.x + self.wingSizeX
            self.left_wing_rect.x = self.rect.x
            self.right_wing_rect.x = self.rect.x + self.wingSizeX + self.centerSize