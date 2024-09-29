import pygame
import json

from menu.main_menu import * # Used for text formatting
from user_save_and_load import save_state

def save_game(save_state, filename):
    # Will write all variables in save_state to a json file to be accessed
    
    draw_text('Game Saved', font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 100)
    print("Saving is WIP")
