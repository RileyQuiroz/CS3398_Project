import pygame
import json
import os

def load_game(filename):
    # Attempt to load the desired save file
    file_path = os.path.join('savesystem/savedata', filename)
    if os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as load_file:
            game_state = json.load(load_file)
        print("Load success")
        return game_state, pygame.time.get_ticks()
    print("No savedata")
    return None, pygame.time.get_ticks()