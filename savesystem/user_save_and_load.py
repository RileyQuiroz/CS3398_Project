import pygame
import sys

from save_progress import *
from load_progress import *
# will import all variables to be saved when they exist from the file they exist under

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BULLETHELL")

save_state = {
    # Temporary variable names, will change and add more according to other files
    # Saved values will also be changed to reflect in-game values once those parts of code are finished
    "player_health": 3,
    "current_level": 0,
    "current_weapon": 0,
    "ship_color": 0,
    "score": 0
}

# Users will be given the oportunity to save after every level completes or when they quit
# File gets called by main game, then runs either save or load
# structured as is so that testing is possible on my branches
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_game(save_state, 'save_data_one.json') # named in case we have multiple
            if event.key == pygame.K_l:
                loaded_game = load_game('save_data_one.json')
                if loaded_game: #only completes the load if it was successful
                    save_state = loaded_game
    pygame.display.update()

