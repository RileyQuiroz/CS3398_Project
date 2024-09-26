import pygame
import json

from save_progress import *
from load_progress import *
# will import all variables to be saved when they exist from the file they exist under



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
# structured as is so that testing is possible on my branch
for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s:
            save_game()
        if event.key == pygame.K_l:
            load_game()

