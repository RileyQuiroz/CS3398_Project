import pygame
from gamestates.GameState import GameState
from tools.colors import Colors
from tools.sounds import Sounds

class SettingsState(GameState):
    def __init__(self, game):
        super().__init__(game)
    
    def update(self, game):
        game.change_state('play') # Temorary
     