import pygame
import sys
from timer import Timer

# Initialize pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BULLETHELL")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define font
font = pygame.font.Font(None, 74)

# Define in-game timer
timer = Timer()
timer.stopped = False

# Define menu options
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)
    return text_rect  # Return the rectangle of the text for collision detection

def main_menu():
    while True:
        screen.fill(WHITE)

        # Update in-game timer
        timer.update(1.0)

        # Draw menu options and get their rects for collision detection
        start_game_rect = draw_text('Start Game', font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 100)
        records_rect = draw_text('Records', font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 50)
        settings_rect = draw_text('Settings', font, BLACK, screen, WIDTH // 2, HEIGHT // 2)
        quit_rect = draw_text('Quit', font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 50)
        timer_rect = draw_text(str(timer.elapsed_time), font, BLACK, screen, 75, 30)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_game_rect.collidepoint(event.pos):
                    # Start the game here
                    print("Start Game clicked!")
                    # You can call your game loop or switch to the game scene here.
                elif records_rect.collidepoint(event.pos):
                    print("Records clicked!")
                    # Add logic for Records screen
                elif settings_rect.collidepoint(event.pos):
                    print("Settings clicked!")
                    # Add logic for Settings screen
                elif timer_rect.collidepoint(event.pos):
                    # Add logic for stopping and starting the timer.
                    timer.stopped = not timer.stopped
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Update the display
        pygame.display.update()