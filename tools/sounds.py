import pygame

pygame.mixer.init()

class Sounds:
    # Load hover sound
    hover = pygame.mixer.Sound('assets/sound_efx/hover_sound.wav')

    # Enemy sounds
    ship_destroyed = pygame.mixer.Sound('assets/sound_efx/enemy_down.wav')
    ship_destroyed .set_volume(.35)

    enemy_shot = pygame.mixer.Sound('assets/sound_efx/enemy_shot.wav')
    enemy_shot.set_volume(.2)

    enemy_hurt = pygame.mixer.Sound('assets/sound_efx/enemy_hurt.wav')
    enemy_hurt.set_volume(.5)

    player_hurt = pygame.mixer.Sound('assets/sound_efx/enemy_hurt.wav')
    player_hurt.set_volume(.10)