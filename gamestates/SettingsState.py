import sys
import pygame
from gamestates.GameState import GameState
from tools.colors import Colors
from tools.sounds import Sounds

class SettingsState(GameState):
    def __init__(self, game):
        super().__init__(game)

        self.hovered = {
            'easy': False,
            'normal': False,
            'hard': False,
            'back': False
        }

        self.rect_colors = {
            'easy': Colors.WHITE,
            'normal': Colors.WHITE,
            'hard': Colors.WHITE,
            'back': Colors.WHITE
        }

        self.easy_rect = game.draw_text_left_aligned('Easy', game.SMALLER_FONT, self.rect_colors['easy'], 300, game.HEIGHT // 2 - 50)
        self.medium_rect = game.draw_text_left_aligned('Normal', game.SMALLER_FONT, self.rect_colors['normal'], 450, game.HEIGHT // 2 - 50)
        self.hard_rect = game.draw_text_left_aligned('Hard', game.SMALLER_FONT, self.rect_colors['hard'], 650, game.HEIGHT // 2 - 50)
        self.back_rect = game.draw_text('Back', game.MAIN_FONT, self.rect_colors['back'], game.WIDTH // 2, game.HEIGHT // 2 + 250)
        self.difficulty_label = 'Easy'
        self.change_message_display_time = 0

    def update(self, game):
        mouse_pos = pygame.mouse.get_pos()

        if self.back_rect.collidepoint(mouse_pos):
            if not self.hovered['back']:
                Sounds.hover.play()
                self.hovered['back'] = True
        else:
            self.hovered['back'] = False

        if self.easy_rect.collidepoint(mouse_pos):
            if not self.hovered['easy']:
                Sounds.hover.play()
                self.hovered['easy'] = True
        else:
            self.hovered['easy'] = False

        if self.medium_rect.collidepoint(mouse_pos):
            if not self.hovered['normal']:
                Sounds.hover.play()
                self.hovered['normal'] = True
        else:
            self.hovered['normal'] = False

        if self.hard_rect.collidepoint(mouse_pos):
            if not self.hovered['hard']:
                Sounds.hover.play()
                self.hovered['hard'] = True
        else:
            self.hovered['hard'] = False

        for rect in self.rect_colors:
            self.rect_colors[rect] = Colors.NEON_PURPLE if self.hovered[rect] else Colors.WHITE

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.hovered['easy']:
                    game.difficulty = 0
                    self.difficulty_label = 'Easy'
                    self.change_message_display_time = 5000
                elif self.hovered['normal']:
                    game.difficulty = 1
                    self.difficulty_label = 'Normal'
                    self.change_message_display_time = 5000
                elif self.hovered['hard']:
                    game.difficulty = 2
                    self.difficulty_label = 'Hard'
                    self.change_message_display_time = 5000
                elif self.hovered['back']:
                    game.change_state('main_menu')

    def draw(self, game):
        game.screen.blit(game.background, (0, 0))

        # Display a simple "Settings" title and "Back" option
        game.draw_text('Settings', game.MAIN_FONT, Colors.WHITE, game.WIDTH // 2, game.HEIGHT // 2 - 250)

        # Display the "Difficulty" label
        game.draw_text_left_aligned('Difficulty', game.SMALLER_FONT, Colors.WHITE, 50, game.HEIGHT // 2 - 50)

        # Display the game difficulty options
        self.easy_rect = game.draw_text_left_aligned('Easy', game.SMALLER_FONT, self.rect_colors['easy'], 300, game.HEIGHT // 2 - 50)
        self.medium_rect = game.draw_text_left_aligned('Normal', game.SMALLER_FONT, self.rect_colors['normal'], 450, game.HEIGHT // 2 - 50)
        self.hard_rect = game.draw_text_left_aligned('Hard', game.SMALLER_FONT, self.rect_colors['hard'], 650, game.HEIGHT // 2 - 50)

        # Display the back button
        self.back_rect = game.draw_text('Back', game.MAIN_FONT, self.rect_colors['back'], game.WIDTH // 2, game.HEIGHT // 2 + 250)

        if self.change_message_display_time > 0:
            game.draw_text('Difficulty: ' + self.difficulty_label, game.SMALL_FONT, Colors.NEON_CYAN, game.WIDTH - 200, 25)
            self.change_message_display_time -= 10