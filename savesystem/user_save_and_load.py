import pygame
import sys

from save_progress import *
from load_progress import *
# will import all variables to be saved when they exist from the file they exist under

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BULLETHELL")
WHITE = (255, 255, 255)
font = pygame.font.Font("assets/fonts/Future Edge.ttf", 30)
clock = pygame.time.Clock()

save_state = {
    # Temporary variable names, will change and add more according to other files
    # Saved values will also be changed to reflect in-game values once those parts of code are finished
    "player_health": 3,
    "current_level": 0,
    "current_weapon": 0,
    "ship_color": 0,
    "score": 0,
    "finish_time": 0
}

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)
    return text_rect

# Users will be given the oportunity to save after every level completes or when they quit
# File gets called by main game, then runs either save or load
# structured as is so that testing is possible on my branches
running = True
text_show = False
while running:
    screen.fill((0, 0, 0)) # Clears screen :)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                start_time = save_game(save_state, 'save_data_one.json') # named in case we have multiple
                text_show = True
                message = 'Game Saved'
            if event.key == pygame.K_l:
                loaded_game, start_time = load_game('save_data_one.json')
                text_show = True
                if loaded_game: #only completes the load if it was successful
                    save_state = loaded_game
                    message = 'Save loaded'
                else:
                    message = 'No save data found'
    # Keeps message on screen for 1.5 seconds
    current_time = pygame.time.get_ticks()
    if text_show and current_time - start_time < 1500:
        draw_text(message, font, WHITE, screen, WIDTH // 2 - 200, HEIGHT // 2 + 275)
    else:
        text_show = False  

    pygame.display.flip()
    clock.tick(60)

