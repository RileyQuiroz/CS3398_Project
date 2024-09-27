import pygame
import sys

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

# Define menu options
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def main_menu():
    while True:
        screen.fill(WHITE)

        # Draw menu options
        # added rectangles around the options for boundry detection
        draw_text('Start Game', font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 100)
        draw_text('Records', font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text('Settings', font, BLACK, screen, WIDTH // 2, HEIGHT // 2)
        draw_text('Quit', font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 50)

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

        # Update the display
        pygame.display.update()

# Call the main menu function
if __name__ == "__main__":
    main_menu()
