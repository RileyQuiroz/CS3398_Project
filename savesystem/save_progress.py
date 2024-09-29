import json
import os

from menu.main_menu import * # Used for draw_text formatting

def save_game(save_state, filename):
    # Will write all variables in save_state to a json file to be accessed later
    file_path = os.path.join('savedata', filename)
    with open(file_path, 'w') as save_file:
        json.dump(save_state, save_file)
    draw_text('Game Saved', font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 100)
    print("Saving is WIP")
