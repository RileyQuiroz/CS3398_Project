import json
import os

from menu.main_menu import * # Used for draw_text formatting

def load_game(filename):
    # Attempt to load the desired save file
    file_path = os.path.join('savedata', filename)
    if os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as load_file:
            game_state = json.load(load_file)
        draw_text('Save loaded', font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 100)
        print("Load success")
        return game_state
    draw_text('No save data found', font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 100)
    print("No savedata")
    return 