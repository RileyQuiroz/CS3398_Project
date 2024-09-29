import pygame
import json

from menu.main_menu import *

def save_game():
    # Will write all variables in save_state to a json file to be accessed
    draw_text('Game Saved', font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 100)
    print("Saving is WIP")
