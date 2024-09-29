import pygame

class ScoreDisplay:
    def __init__(self, screen, font_size=36, color=(255, 255, 255), position=(10, 10)):
        self.screen = screen
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.position = position

    def display_score(self, score):
        score_text = self.font.render(f"Score: {score}", True, self.color)
        self.screen.blit(score_text, self.position)