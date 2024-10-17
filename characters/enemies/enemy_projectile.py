import pygame
class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=5):
        super().__init__()
        self.image = pygame.Surface((5, 10))  # Width 5, height 10 for the projectile
        self.image.fill((255, 255, 255))  # White color for the projectile
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        
    def update(self):
        # Move the projectile down the screen
        self.rect.y += self.speed
        # Remove the projectile if it goes off-screen
        if self.rect.top >= pygame.display.get_surface().get_height():
            self.kill()  # Remove the projectile from the group