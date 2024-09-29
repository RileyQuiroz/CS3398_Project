import pygame

class ScoreDisplay:
    def __init__(self, screen, font_size=36, color=(255, 255, 255), position=(10, 10)) -> None: # Initializes the ScoreDisplay object
        self.screen = screen
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.position = position

    def display_score(self, score) -> None: # Displays the score at specified position (top left, 10 pixels from left and top)
        score_text = self.font.render(f"Score: {score}", True, self.color)
        self.screen.blit(score_text, self.position)