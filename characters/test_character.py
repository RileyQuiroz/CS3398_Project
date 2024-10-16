import pygame
from player_char import CharacterPawn  # Import the CharacterPawn class

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 600))  # Example screen size
pygame.display.set_caption("Character Test")

# Initialize the character
character = CharacterPawn(100, 100)  # Start character at (100, 100)

# Set up the clock for controlling frame rate
clock = pygame.time.Clock()
running = True

# Main test loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle character movement input
    character.handle_input()

    # Clear the screen
    screen.fill((0, 0, 0))  # Black background

    # Draw the character
    character.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to 60 FPS
    clock.tick(60)

# Clean up
pygame.quit()
