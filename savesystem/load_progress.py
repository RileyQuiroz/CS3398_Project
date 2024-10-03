import pygame
import json
import os

#from menu.main_menu import * # Used for draw_text formatting
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
font = pygame.font.Font("assets/fonts/Future Edge.ttf", 74)
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)
    return text_rect

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