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
            proj_a = EnemyProjectileAngled(self.rect.centerx, self.rect.centery, 0, 6)
            proj_b = EnemyProjectileAngled(self.rect.centerx, self.rect.centery, 45, 6)
            proj_c = EnemyProjectileAngled(self.rect.centerx, self.rect.centery, 90, 6)
            proj_d = EnemyProjectileAngled(self.rect.centerx, self.rect.centery, 135, 6)
            proj_e = EnemyProjectileAngled(self.rect.centerx, self.rect.centery, 180, 6)
            proj_f = EnemyProjectileAngled(self.rect.centerx, self.rect.centery, 225, 6)
            proj_g = EnemyProjectileAngled(self.rect.centerx, self.rect.centery, 270, 6)
            proj_h = EnemyProjectileAngled(self.rect.centerx, self.rect.centery, 315, 6)
            # Star burst pattern
            proj_group.add(proj_a)
            proj_group.add(proj_b)
            proj_group.add(proj_c)
            proj_group.add(proj_d)
            proj_group.add(proj_e)
            proj_group.add(proj_f)
            proj_group.add(proj_g)
            proj_group.add(proj_h)
            self.kill()