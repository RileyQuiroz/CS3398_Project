import sys
import pygame

from tools.colors import Colors
from tools.sounds import Sounds
from gamestates.GameState import GameState

class PauseState(GameState):
    def __init__(self, game):
        super().__init__(game)

    def update(self, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game.change_state('play')
                elif event.key == pygame.K_ESCAPE:
                    game.change_state('main_menu')

    def draw(self, game):
        game.states['play'].draw(game)
        game.draw_text('Paused', game.SMALL_FONT, Colors.NEON_CYAN, game.WIDTH // 2, game.HEIGHT // 2)