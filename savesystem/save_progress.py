import pygame
import json
import os

pygame.init()

#from menu.main_menu import * # Used for draw_text formatting
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

def save_game(save_state, filename):
    # Will write all variables in save_state to a json file to be accessed later
    file_path = os.path.join('savesystem/savedata', filename)
    with open(file_path, 'w') as save_file:
        json.dump(save_state, save_file)
    print("Saving is WIP")
    return pygame.time.get_ticks()
