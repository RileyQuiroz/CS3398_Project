import json
import os

from menu.main_menu import * # Used for draw_text formatting

def load_game():
    # Attempt to load a file of the same name as the one in save_progress
    print("Unable to load file")