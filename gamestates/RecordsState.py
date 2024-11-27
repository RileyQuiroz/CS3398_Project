import sys
import pygame
from gamestates.GameState import GameState
from savesystem.leaderboard import Leaderboard
from tools.colors import Colors
from tools.sounds import Sounds

class RecordsState(GameState):
    def __init__(self, game):
        super().__init__(game)

        self.hovered = {
            'back': False
        }

        self.leaderboard = Leaderboard('time_scoreboard.json')
        self.entries = []
        self.back_color = Colors.WHITE
        self.back_rect = game.draw_text('Back', game.MAIN_FONT, self.back_color, game.WIDTH // 2, game.HEIGHT // 2 + 250)

    def enter(self, game):
        self.entries = []

        # Parse the fastest finishing times from the leaderboard
        for i in range(len(self.leaderboard.high_scores)):
            rank = str(i + 1) + '.'
            initials = str(self.leaderboard.high_scores[i][0])
            score = str(self.leaderboard.high_scores[i][1])
            self.entries.append(rank + "\t" + initials + "\t" + score)
 
    def update(self, game):
        mouse_pos = pygame.mouse.get_pos()

        if self.back_rect.collidepoint(mouse_pos):
            if not self.hovered['back']:
                Sounds.hover.play()
                self.hovered['back'] = True
        else:
            self.hovered['back'] = False

        self.back_color = Colors.NEON_PURPLE if self.hovered['back'] else Colors.WHITE

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.hovered['back']:
                    game.change_state('main_menu')

    def draw(self, game):
        # Display a simple "Records" title and "Back" option
        game.draw_text('Records', game.MAIN_FONT, Colors.WHITE, game.WIDTH // 2, game.HEIGHT // 2 - 250)

        # Display each entry in the leaderboard
        for i, entry in enumerate(self.entries):
            game.draw_text(entry, game.MAIN_FONT, Colors.WHITE, game.WIDTH // 2, game.HEIGHT // 3.5 + (80 * i))

        # Display the back button
        self.back_rect = game.draw_text('Back', game.MAIN_FONT, self.back_color, game.WIDTH // 2, game.HEIGHT // 2 + 250)
