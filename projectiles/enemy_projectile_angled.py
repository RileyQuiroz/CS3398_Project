import pygame
import math
class EnemyProjectileAngled(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=45, speed=3):
        super().__init__()
        self.image = pygame.Surface((5, 5)) # Bullet size and shape
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.angle = math.radians(angle) 
        self.x_speed = self.speed * math.cos(self.angle)  # Horizontal speed
        self.y_speed = self.speed * math.sin(self.angle)  # Vertical speed
        
    def update(self, paused):
        # Move the projectile down the screen
        if (paused == False):
            self.rect.y += self.y_speed # will change to move based on angle
            self.rect.x += self.x_speed
        # Remove the projectile if it goes off-screen
        if self.rect.top >= pygame.display.get_surface().get_height():
            self.kill()