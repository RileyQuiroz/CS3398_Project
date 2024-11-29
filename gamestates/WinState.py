import sys
import pygame

from tools.colors import Colors
from tools.sounds import Sounds
from tools.end_screen import EndScreen
from tools.game_states import GameState as WinLoseState
from gamestates.GameState import GameState

class WinState(GameState):
    def __init__(self, game):
        super().__init__(game)
        
        self.end_screen = EndScreen(game.screen, game.player)

    def update(self, game):
        position = game.leaderboard.compare_score(game.win_lose_system.score_system.score)

        if position is not None:
            initials = game.enter_initials(game.MAIN_FONT, position, game.win_lose_system.score_system.score)

            game.leaderboard.update_list(position, initials, game.win_lose_system.score_system.score)
            game.leaderboard.save()
        
            print("Updated Leaderboard:")
            for entry in game.leaderboard.high_scores:
                print(f"{entry[0]}: {entry[1]}")

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
                        game.reset()
                        game.change_state('play')
                    elif selected_option == "Main Menu":
                        end_screen_display = False
                        game.reset()
                        game.change_state('main_menu')
                    elif selected_option == "Quit":
                        pygame.quit()
                        exit()
  
    def draw(self, game):
        self.end_screen.display(WinLoseState.WIN)
