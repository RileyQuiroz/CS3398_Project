import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
from projectiles.projectiles import Projectile

class CharacterPawn:
    def __init__(self, x, y, projectiles_group, screen_width, screen_height, health=100, shield=100):
        # Initialize character position, movement attributes, and screen dimensions
        self.x = x
        self.y = y
        self.speed = 4.5
        self.width = 20
        self.height = 30
        self.projectiles_group = projectiles_group  # Group for handling projectiles
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Player collision rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # Stats
        self.health = health
        self.is_alive = True
        # Cooldown to prevent spamming bullets
        self.last_shot_time = pygame.time.get_ticks()
        self.shot_cooldown = 250  # in milliseconds
        self.last_enemy_collision = 0
        self.got_hit = False
        self.shield = 0

    def handle_input(self, stopped):
        # Handle basic movement input
        keys = pygame.key.get_pressed()
        if(stopped == False):
            if keys[pygame.K_LEFT]:
                self.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.x += self.speed
            if keys[pygame.K_UP]:
                self.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.y += self.speed

        # Boundary conditions
        self.x = max(0, min(self.screen_width - self.width, self.x))
        self.y = max(0, min(self.screen_height - self.height, self.y))

        # Update the rect position
        self.rect.topleft = (self.x, self.y)

    def shoot(self, stopped):
        # Add a delay between shots
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shot_cooldown and stopped == False:
            bullet = Projectile(self.x + self.width // 2, self.y)  # Center the projectile
            self.projectiles_group.add(bullet)
            self.last_shot_time = current_time

    def draw(self, screen, curr_time):
        # Determine color based on health
        color = (255, 255, 0) if self.health < 50 else (0, 255, 0)
        if(self.got_hit):
            color = (255,255,255)
        pygame.draw.rect(screen, color, self.rect)
        # Draw health bar
        self.draw_health_bar(screen)
        self.draw_shield_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = 200
        bar_height = 20
        fill = (self.health / 100) * bar_width
        health_bar = pygame.Rect(10, self.screen_height - bar_height - 10, bar_width, bar_height)
        health_fill = pygame.Rect(10, self.screen_height - bar_height - 10, fill, bar_height)

        pygame.draw.rect(screen, (255, 0, 0), health_bar)  # Red background for health bar
        pygame.draw.rect(screen, (0, 255, 0), health_fill)  # Green fill for current health

    def draw_shield_bar(self, screen):
        bar_width = 200
        bar_height = 20
        fill = (self.shield / 100) * bar_width
        # Position shield bar just above the health bar
        shield_bar = pygame.Rect(10, self.screen_height - 2 * bar_height - 20, bar_width, bar_height)
        shield_fill = pygame.Rect(10, self.screen_height - 2 * bar_height - 20, fill, bar_height)

        pygame.draw.rect(screen, (0, 0, 255), shield_bar)  # Blue background for shield bar
        pygame.draw.rect(screen, (0, 255, 255), shield_fill)  # Cyan fill for current shield


    def take_dmg(self, amount):
        if self.shield > 0:
            self.shield -= 25
        else:
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.is_alive = False

    def heal(self, amount):
        if self.is_alive:
            self.health = min(100, self.health + amount)
    
    def consume(self, consumable):
        if consumable == "repair_kit":
            # Heal to max but respect current health limit
            self.health = min(100, self.health + 100)
        elif consumable == "shield_pack":
            # Recharge shield to max but respect shield limit
            self.shield = min(100, self.shield + 100)

class Consumable(pygame.sprite.Sprite):
    def __init__(self, x, y, consumable_type):
        super().__init__()
        self.x = x
        self.y = y
        self.consumable_type = consumable_type  # this can be "repair_kit" or "shield_pack"
        self.image = pygame.Surface((20,20))
        self.image.fill((0, 255, 255) if consumable_type == "shield_pack" else (255, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
