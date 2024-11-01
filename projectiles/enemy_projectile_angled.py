import pygame
class EnemyProjectileAngled(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=3):
        super().__init__()
        self.image = pygame.Surface((5, 5)) # Bullet size and shape
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.angle = 45
        
    def update(self, paused):
        # Move the projectile down the screen
        if (paused == False):
            self.rect.y += self.speed # will change to move based on angle
        # Remove the projectile if it goes off-screen
        if self.rect.top >= pygame.display.get_surface().get_height():
            self.kill()