import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = 7
        self.width = 5
        self.height = 10
        self.color = (0, 255, 0)  # Bullet color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        # Move the bullet upwards
        self.rect.y -= self.speed

    def update(self):
        self.move()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
