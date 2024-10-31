import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
from projectiles.projectiles import Projectile

class CharacterPawn:
    def __init__(self, x, y, projectiles_group, screen_width, screen_height):
        # Initialize character position, movement attributes, and screen dimensions
        self.x = x
        self.y = y
        self.speed = 5
        self.width = 40
        self.height = 60
        self.projectiles_group = projectiles_group  # Group for handling projectiles
        self.screen_width = screen_width
        self.screen_height = screen_height

    def handle_input(self):
        # Handle basic movement input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        # Boundary conditions
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > self.screen_width:
            self.x = self.screen_width - self.width

        if self.y < 0:
            self.y = 0
        elif self.y + self.height > self.screen_height:
            self.y = self.screen_height - self.height

    def shoot(self):
        # Fire a projectile and add it to the projectiles group
        bullet = Projectile(self.x + self.width // 2, self.y)  # Center the projectile
        self.projectiles_group.add(bullet)

    def draw(self, screen):
        # Draw character pawn on the screen
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))
