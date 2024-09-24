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

        # Get mouse position and events
        mx, my = pygame.mouse.get_pos()

        # Draw menu options
        draw_text('Start Game', font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text('Quit', font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 50)
    

        # Handle mouse clicks for menu interaction
        click = pygame.mouse.get_pressed()
        if WIDTH // 2 - 100 < mx < WIDTH // 2 + 100:
            if HEIGHT // 2 - 75 < my < HEIGHT // 2 - 25 and click[0] == 1:
                # Start game logic
                print("Starting Game...")
            if HEIGHT // 2 + 25 < my < HEIGHT // 2 + 75 and click[0] == 1:
                pygame.quit()
                sys.exit()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update the display
        pygame.display.update()

# Call the main menu function
if __name__ == "__main__":
    main_menu()
