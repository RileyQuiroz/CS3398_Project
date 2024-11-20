import pygame
import sys
import random
from tools.timer import Timer
from tools.score_counter import Score
from tools.score_display import ScoreDisplay
from tools.collision_hanlder import *
from savesystem.leaderboard import Leaderboard
from savesystem import user_save_and_load
from tools.game_states import GameState
from tools.end_screen import EndScreen
from tools.win_lose_system import WinLoseSystem
from characters.player_char import CharacterPawn
from characters.enemies.enemy_spawn_and_despawn import spawnEnemy, despawnEnemy, startRetreat, destroyEnemy
from tools.collision_hanlder import check_projectile_enemy_collisions, check_player_projectile_collisions
from tools.Star_and_planet_bg_logic import Background
from characters.player_char import Consumable
#import obstacles
from obstacles import *

class Colors:
    NEON_CYAN = (0, 255, 255)
    NEON_PURPLE = (155, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

class Sounds:
    # Load hover sound
    hover = pygame.mixer.Sound("assets/sound_efx/hover_sound.wav")  # Replace with your sound file

    # Enemy sounds
    ship_destroyed = pygame.mixer.Sound("assets/sound_efx/enemy_down.wav")
    ship_destroyed .set_volume(.35)
    enemy_shot = pygame.mixer.Sound("assets/sound_efx/enemy_shot.wav")
    enemy_shot.set_volume(.2)
    enemy_hurt = pygame.mixer.Sound("assets/sound_efx/enemy_hurt.wav")
    enemy_hurt.set_volume(.15)

class Game:
    # Define screen dimensions
    WIDTH = 800
    HEIGHT = 600

    # Define fonts
    MAIN_FONT = pygame.font.Font("assets/fonts/Future Edge.ttf", 74)
    SMALLER_FONT = pygame.font.Font("assets/fonts/Future Edge.ttf", 34)

    # Define frame rate
    FPS = 60

    BOULDER_PATH = "assets/objects/spr_boulder_0.png"

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Initialize screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("BULLETHELL")

        # Initialize start menu background
        bg_image = pygame.image.load("assets/backgrounds/space_background4.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        # Initialize leaderboard
        self.leaderboard = Leaderboard("time_scoreboard.json")

        # Initialize in-game clock and timer
        self.clock = pygame.time.Clock()
        self.timer = Timer()
        #timer.start()

        # Initialize score system
        self.score_system = Score()
        self.score_display = ScoreDisplay()

        # Initialize win-lose system
        self.win_lose_system = WinLoseSystem()

        # Initialize groups
        self.proj_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        self.set_obstacles()

        # Initialize player
        self.player = CharacterPawn(
            x=self.WIDTH // 2,
            y=self.HEIGHT - 100,
            projectiles_group=self.proj_group,
            screen_width=self.WIDTH,
            screen_height=self.HEIGHT
        )

        self.win_lose_system.player = self.player

        # Initialize game states
        self.states = {

        }

    # Define menu options
    def draw_text(self, text, font, color, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_obj, text_rect)
        return text_rect

    def draw_text_left_aligned(self, text, font, color, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(topleft=(x, y))  # Align to the left (top-left corner)
        self.screen.blit(text_obj, text_rect)
        return text_rect

    def set_obstacles(self): 
        BOULDER_PATH = "assets/objects/spr_boulder_0.png"
        
        self.obstacle_group.add(Mover((200, 200), (10, 10), BOULDER_PATH))
        self.obstacle_group.add(Rotator((200, 400), BOULDER_PATH))
        self.obstacle_group.add(ZigZag((0, 300), (50, 0), BOULDER_PATH))
        self.obstacle_group.add(Dangerous((500, 550), BOULDER_PATH))
        self.obstacle_group.add(Destructible((550, 300), 5, BOULDER_PATH))
        self.obstacle_group.add(Friend((100, 200), 5, self.score_system, BOULDER_PATH))

    def reset(self):
        self.score_system.reset()
        self.timer.reset()
        self.player.heal(100)
        self.player.is_alive = True
        self.win_lose_system.reset()
        self.proj_group.empty()
        self.enemy_group.empty()  # Clear all enemies
        self.obstacle_group.empty()
        self.enemy_projectiles.empty()
        self.timer.start()
        self.set_obstacles() # Temporary
        self.player.x = self.WIDTH // 2
        self.player.y = self.HEIGHT - 100
