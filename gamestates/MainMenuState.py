import sys
import pygame

from tools.colors import Colors
from tools.sounds import Sounds
from gamestates.GameState import GameState

class MainMenuState(GameState):
    def __init__(self, game):
        super().__init__(game)

        # Draw main menu options with updated hover colors
        self.start_color = (0, 0, 0)
        self.records_color = (0, 0, 0)
        self.settings_color = (0, 0, 0)
        self.quit_color = (0, 0, 0)
        self.start_game_rect = pygame.rect.Rect(0, 0, 0, 0)
        self.records_rect = pygame.rect.Rect(0, 0, 0, 0)
        self.settings_rect = pygame.rect.Rect(0, 0, 0, 0)
        self.quit_rect = pygame.rect.Rect(0, 0, 0, 0)
        self.current_menu = 'main'
        self.hovered = {
            'start_game': False,
            'records': False,
            'settings': False,
            'quit': False,
            'back': False  # Hover state for the 'Back' option in other menus
        }

    def update(self, game):
        mouse_pos = pygame.mouse.get_pos()

        # Hover and sound logic for the main menu
        if self.start_game_rect.collidepoint(mouse_pos):
            if not self.hovered['start_game']:
                Sounds.hover.play()
                self.hovered['start_game'] = True
        else:
            self.hovered['start_game'] = False

        if self.records_rect.collidepoint(mouse_pos):
            if not self.hovered['records']:
                Sounds.hover.play()
                self.hovered['records'] = True
        else:
            self.hovered['records'] = False

        if self.settings_rect.collidepoint(mouse_pos):
            if not self.hovered['settings']:
                Sounds.hover.play()
                self.hovered['settings'] = True
        else:
            self.hovered['settings'] = False

        if self.quit_rect.collidepoint(mouse_pos):
            if not self.hovered['quit']:
                Sounds.hover.play()
                self.hovered['quit'] = True
        else:
            self.hovered['quit'] = False

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check which option is clicked and switch to the respective menu
                if self.start_game_rect.collidepoint(event.pos):
                    print("Start Game clicked!")
                    game.timer.reset()  # Reset timer when starting a new game
                    game.change_state('play')
                elif self.records_rect.collidepoint(event.pos):
                    game.change_state('records') # Switch to Records menu
                elif self.settings_rect.collidepoint(event.pos):
                    game.change_state('settings') # Switch to Settings menu
                elif self.quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

                #elif current_menu in ['records', 'settings']:
                    # Handle "Back" button in Records or Settings
                #    if self.back_rect.collidepoint(event.pos):
                #        game.change_state('main_menu') # Switch back to Main menu

        # Check if mouse is hovering over the options and set color accordingly
        self.start_color = Colors.NEON_PURPLE if self.hovered['start_game'] else Colors.WHITE
        self.records_color = Colors.NEON_PURPLE if self.hovered['records'] else Colors.WHITE
        self.settings_color = Colors.NEON_PURPLE if self.hovered['settings'] else Colors.WHITE
        self.quit_color = Colors.NEON_PURPLE if self.hovered['quit'] else Colors.WHITE

    def draw(self, game):
        game.screen.blit(game.background, (0, 0))
        self.start_game_rect = game.draw_text('Start Game', game.MAIN_FONT, self.start_color, game.WIDTH // 2, game.HEIGHT // 2 - 150)
        self.records_rect = game.draw_text('Records', game.MAIN_FONT, self.records_color, game.WIDTH // 2, game.HEIGHT // 2 - 50)
        self.settings_rect = game.draw_text('Settings', game.MAIN_FONT, self.settings_color, game.WIDTH // 2, game.HEIGHT // 2 + 50)
        self.quit_rect = game.draw_text('Quit', game.MAIN_FONT, self.quit_color, game.WIDTH // 2, game.HEIGHT // 2 + 150)
