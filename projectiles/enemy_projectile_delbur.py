import pygame
from projectiles.enemy_projectile_angled import EnemyProjectileAngled
class EnemyProjectileDelayBurst(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, currTime):
        super().__init__()
        self.image = pygame.Surface((7, 7)) # Bullet size and shape
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.spawn_time = currTime
        
    def update(self, paused, proj_group, currTime):
        # Move the projectile down the screen
        if (paused == False):
            self.rect.y += self.speed
        # Projectile bursts after 1 second of travel
        if currTime-self.spawn_time >= 1:
            # Star burst pattern
            currAngle = 0
            while currAngle < 360:
                newProj = EnemyProjectileAngled(self.rect.centerx, self.rect.centery, currAngle, 6)
                proj_group.add(newProj)
                currAngle += 45
            self.kill()