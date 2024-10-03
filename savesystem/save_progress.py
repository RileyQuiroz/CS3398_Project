import pygame
import json
import os

pygame.init()

def save_game(save_state, filename):
    # Will write all variables in save_state to a json file to be accessed later
    file_path = os.path.join('savesystem/savedata', filename)
    with open(file_path, 'w') as save_file:
        json.dump(save_state, save_file)
    print("Saving is WIP")
    return pygame.time.get_ticks()
