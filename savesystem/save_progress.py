import pygame
import json

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

def save_game():
    # Will write all variables in save_state to a json file to be accessed
    print("Saving is WIP")
