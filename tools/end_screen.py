import pygame
from tools.game_states import GameState

class EndScreen:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.Font("assets/fonts/Future Edge.ttf", 74)
        self.smaller_font = pygame.font.Font("assets/fonts/Future Edge.ttf", 34)
        self.options = ["Restart", "Main Menu", "Quit"]
        self.hovered = {"Restart": False, "Main Menu": False, "Quit": False}

    def display(self, game_state):
        self.screen.fill((0, 0, 0))
        message = "YOU WIN!" if game_state == GameState.WIN else "DEFEATED!"
        if game_state == GameState.WIN:
            message_surface = self.font.render(message, True, (0, 255, 0))
        elif game_state == GameState.LOSE:
            message_surface = self.font.render(message, True, (255, 0, 0))
        self.screen.blit(message_surface, (400 - message_surface.get_width() // 2, 200))

        # Draw options with hover color
        mouse_pos = pygame.mouse.get_pos()
        for i, option in enumerate(self.options):
            color = (155, 0, 255) if self.hovered[option] else (255, 255, 255)
            option_surface = self.smaller_font.render(option, True, color)
            option_rect = option_surface.get_rect(center=(400, 300 + i * 50))
            self.screen.blit(option_surface, option_rect)

            # Check if hovered and play sound
            if option_rect.collidepoint(mouse_pos):
                if not self.hovered[option]:
                    pygame.mixer.Sound("assets/sound_efx/hover_sound.wav").play()
                    self.hovered[option] = True
            else:
                self.hovered[option] = False

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.check_option_click(pygame.mouse.get_pos())

    def check_option_click(self, pos):
        # Check which option was clicked and call the respective callback
        for i, option in enumerate(self.options):
            option_surface = self.smaller_font.render(option, True, (255, 255, 255))
            option_rect = option_surface.get_rect(center=(400, 300 + i * 50))
            if option_rect.collidepoint(pos):
                return option
