import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame
from projectiles.projectiles import Projectile

class CharacterPawn:
    def __init__(self, x, y, projectiles_group):
        # Initialize character position and movement attributes
        self.x = x
        self.y = y
        self.speed = 5
        self.width = 40
        self.height = 60
        self.projectiles_group = projectiles_group  # Group for handling projectiles

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

        # Handle shooting
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        # Fire a projectile and add it to the projectiles group
        bullet = Projectile(self.x + self.width // 2, self.y)  # Center the projectile
        self.projectiles_group.add(bullet)

    def draw(self, screen):
        # Draw character pawn on the screen
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))
