import pygame
import sys
import random
from tools.timer import Timer
from tools.score_counter import Score
from tools.score_display import ScoreDisplay
from tools.collision_hanlder import *
from savesystem.leaderboard import Leaderboard
from savesystem import user_save_and_load
from obstacles.Mover import Mover
from obstacles.Rotator import Rotator
from obstacles.ZigZag import ZigZag
from obstacles.Dangerous import Dangerous
from obstacles.Destructible import Destructible
from obstacles.Friend import Friend
from tools.game_states import GameState
from tools.end_screen import EndScreen
from tools.win_lose_system import WinLoseSystem
from characters.player_char import CharacterPawn
from characters.enemies.enemy_spawn_and_despawn import spawnEnemy, despawnEnemy, startRetreat, destroyEnemy
from tools.collision_hanlder import check_projectile_enemy_collisions, check_player_projectile_collisions
from tools.Star_and_planet_bg_logic import Background
from characters.player_char import Consumable, spawn_consumable

from gamestates.Game import *
from gamestates.GameState import GameState

class PlayState(GameState):
    def __init__(self, game):
        pass
    
    def enter(self, game):
        pass

    def update(self, game):
        pass

    def draw(self, game):
        pass

    def leave(self, game):
        pass
