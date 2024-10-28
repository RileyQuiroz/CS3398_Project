import pygame
from characters.player_char import CharacterPawn  # Import the CharacterPawn class
from characters.enemies.enemy_structure import Enemy  # Import the Enemy class
from tools.collision_hanlder import check_projectile_enemy_collisions  # Import collision handler

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 600))  # Example screen size
pygame.display.set_caption("Character and Collision Test")

# Initialize sprite groups
projectiles = pygame.sprite.Group()  # Group for projectiles
enemies = pygame.sprite.Group()

# Initialize the character
character = CharacterPawn(100, 100, projectiles)  # Pass projectiles group to the character

# Initialize an enemy for testing
enemy = Enemy(x=300, y=100)  # Create an enemy at position (300, 100)
enemies.add(enemy)

# Set up the clock for controlling frame rate
clock = pygame.time.Clock()
running = True

# Main test loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle character movement and shooting input
    character.handle_input()

    # Update all projectiles
    projectiles.update()

    # Check for projectile-enemy collisions
    check_projectile_enemy_collisions(projectiles, enemies)

    # Clear the screen
    screen.fill((0, 0, 0))  # Black background

    # Draw the character and enemies
    character.draw(screen)
    enemies.draw(screen)
    projectiles.draw(screen)  # Draw all projectiles

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to 60 FPS
    clock.tick(60)

# Clean up
pygame.quit()
