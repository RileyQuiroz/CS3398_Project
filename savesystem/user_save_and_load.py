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

# Users will be given the oportunity to save after every level completes