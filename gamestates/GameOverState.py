import sys
import pygame

from tools.colors import Colors
from tools.sounds import Sounds
from tools.end_screen import EndScreen
from tools.game_states import GameState as WinLoseState
from gamestates.GameState import GameState

class GameOverState(GameState):
    def __init__(self, game):
        super().__init__(game)
        
        self.end_screen = EndScreen(game.screen, game.player)

    def update(self, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = event.pos
                    selected_option = self.end_screen.check_option_click(pos)
                    if selected_option == "Restart":
                        end_screen_display = False
                        game.change_state('play')
                    elif selected_option == "Main Menu":
                        end_screen_display = False
                        game.change_state('main_menu')
                    elif selected_option == "Quit":
                        pygame.quit()
                        exit()
  
    def draw(self, game):
        self.end_screen.display(WinLoseState.LOSE)
