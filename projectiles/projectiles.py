import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=7, color=(0, 255, 0), size=(5, 10), damage = 1):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.width, self.height = size
        self.color = color  # Bullet color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        # Move the bullet upwards
        self.rect.y -= self.speed

    def update(self, stopped, *args):
        if not stopped:
            self.move()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
