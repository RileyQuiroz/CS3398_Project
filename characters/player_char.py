import pygame

class CharacterPawn:
    def __init__(self, x, y):
        # Initialize character position and movement attributes
        self.x = x
        self.y = y
        self.speed = 5
        self.width = 40
        self.height = 60

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

    def draw(self, screen):
        # Draw character pawn on the screen
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))
