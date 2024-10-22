import pygame
class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=3):
        super().__init__()
        self.image = pygame.Surface((5, 5)) # Bullet size and shape
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        
    def update(self):
        # Move the projectile down the screen
        self.rect.y += self.speed
        # Remove the projectile if it goes off-screen
        if self.rect.top >= pygame.display.get_surface().get_height():
            self.kill()