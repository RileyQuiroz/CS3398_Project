import sys
import random
import pygame
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
from tools.collision_hanlder import check_projectile_enemy_collisions, check_player_projectile_collisions, check_player_consumable_collisions
from tools.Star_and_planet_bg_logic import Background, EvilBackground
from tools.bonus_objectives import BonusObjective, NoDamageObjective, AccuracyObjective, UnderTimeObjective, KillStreakObjective, BonusObjectiveDisplay
from tools.colors import Colors

from characters.player_char import Consumable
from obstacles import *
from gamestates import *

pygame.init()

class Game:
    # Define screen dimensions
    WIDTH = 800
    HEIGHT = 600

    # Define fonts
    MAIN_FONT = pygame.font.Font("assets/fonts/Future Edge.ttf", 74)
    SMALLER_FONT = pygame.font.Font("assets/fonts/Future Edge.ttf", 34)
    SMALL_FONT = pygame.font.Font("assets/fonts/Future Edge.ttf", 32)

    # Define frame rate
    FPS = 60

    BOULDER_PATH = "assets/objects/spr_boulder_0.png"

    def __init__(self):
        # Initialize screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("BULLETHELL")

        # Initialize start menu background
        bg_image = pygame.image.load("assets/backgrounds/space_background4.png")
        self.background = pygame.transform.scale(bg_image, (self.WIDTH, self.HEIGHT))

        # Initialize leaderboard
        self.leaderboard = Leaderboard("time_scoreboard.json")

        # Initialize in-game clock and timer
        self.clock = pygame.time.Clock()
        self.timer = Timer()
        
        # Initialize ticks and delta time.
        self.ticks = pygame.time.get_ticks()
        self.ticks_last_frame = 0.0
        self.delta_time = 0.0

        # Initialize score system
        self.score_system = Score()
        self.score_display = ScoreDisplay(self.screen, font_size=36, color=Colors.NEON_CYAN, position=(50, 50))

        # Initialize win-lose system
        self.win_lose_system = WinLoseSystem(self.score_system, player=None)

        # Initialize groups
        self.proj_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
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
        self.win_lose_system.current_level = 0

        # Assign and initialize objectives
        self.current_objectives = self.assign_bonus_objectives()
        for obj in self.current_objectives:
            obj.initialize(self.player, self.win_lose_system) # FIXME: current_level being passed isn't right or works

        # Display objectives
        #print("Bonus Objectives for this level:")
        #for obj in self.current_objectives:
        #    print(f"- {obj.description}")
            #IMPORTANT: TEMP VARIABLEs FOR SAVE SYSTEM, USE/MODIFY FOR WHATEVER YOU NEED

        self.level_cooldown = 5 # Cooldown until level can be progressed, to let levelspawner have time to spawn enemies for current level

        self.objective_display = BonusObjectiveDisplay(self.current_objectives, self.SMALLER_FONT, self.screen)

        self.current_level = 0
        self.lvlThreeSwitch = 0
        self.difficulty = 1     # Game set to normal difficulty by default

        # Initialize game states
        self.states = {
            'main_menu': MainMenuState(self),
            'play': PlayState(self),
            'pause': PauseState(self),
            'win': WinState(self),
            'game_over': GameOverState(self),
            'records': RecordsState(self),
            'settings': SettingsState(self)
        }

        self.previous_state = ''
        self.current_state = 'main_menu'

    # Change between game states
    def change_state(self, next_state):
        if self.states[next_state]:
            self.previous_state = self.current_state
            self.current_state = next_state

            self.states[self.previous_state].leave(self)
            self.states[self.current_state].enter(self)

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
        self.obstacle_group = [
            Mover((200, 200), (10, 10), 0.75, "assets/objects/spr_boulder_0.png"),
            Rotator((200, 400), 2.5, "assets/objects/rotator_obstacle.png"),
            ZigZag((0, 300), (50, 0), 2.5, "assets/objects/obstacle_type_1.png"),
            Dangerous((500, 550), 2.5, "assets/objects/dangerous_obstacle.png"),
            Destructible((550, 300), 5, self.score_system, 2.5, "assets/objects/obstacle_type_2.png"),
            Friend((100, 200), 5, self.score_system, 2.5, "assets/objects/friendly_obstacle.png")
        ]

        for obstacle in self.obstacle_group:
            x_pos = random.uniform(50, self.WIDTH - 50)
            y_pos = random.uniform(50, self.HEIGHT - 50)
            obstacle.position = (x_pos, y_pos)

            # Rotator and ZigZag obstacles require a central point
            # to pivot around
            if hasattr(obstacle, 'center'):
                obstacle.center = obstacle.position

    def assign_bonus_objectives(self):
        """
        Randomly select two bonus objectives from the pool.
        """
        objectives_pool = [
            NoDamageObjective(),
            UnderTimeObjective(),
            AccuracyObjective(),
        ]

        return random.sample(objectives_pool, 2)

    def enter_initials(self, font, position, score):
        """Display an input prompt on the game screen to collect player initials."""
        initials = ""
        clock = pygame.time.Clock()
        running = True

        prompt_font = pygame.font.Font("assets/fonts/Future Edge.ttf", 24)
        initials_font = pygame.font.Font("assets/fonts/Future Edge.ttf", 74)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Press Enter to confirm
                        if len(initials) > 0:
                            running = False
                    elif event.key == pygame.K_BACKSPACE:  # Delete last character
                        initials = initials[:-1]
                    elif len(initials) < 2 and event.unicode.isalpha():  # Limit to 2 letters
                        initials += event.unicode.upper()

            # Clear the screen and display the prompt
            self.screen.fill((0, 0, 0))  # Black background
            prompt_text = f"New High Score! Enter Initials (Score: {score})"
            self.render_text(prompt_font, prompt_text, Colors.NEON_PURPLE, (100, 200))  # Prompt
            self.render_text(initials_font, initials, Colors.NEON_CYAN, (300, 300))  # Current initials
            pygame.display.flip()
            clock.tick(30)

        return initials  # Return the entered initials

    def render_text(self, font, text, color, pos):
        """Render text to the screen."""
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, pos)

    def reset(self):
        self.score_system.reset()
        self.timer.reset()
        self.player.heal(100)
        self.player.is_alive = True
        self.player.player_weapon = "default"
        self.player.shield = 0
        self.win_lose_system.reset()
        self.proj_group.empty()
        self.enemy_group.empty()  # Clear all enemies
        self.enemy_projectiles.empty()
        self.set_obstacles() # Temporary
        self.player.x = self.WIDTH // 2
        self.player.y = self.HEIGHT - 100
        self.current_level = 0
        self.lvlThreeSwitch = 0
        self.clock = pygame.time.Clock()

        self.current_objectives = self.assign_bonus_objectives()
        for obj in self.current_objectives:
            obj.initialize(self.player, self.win_lose_system) # FIXME: current_level being passed isn't right or works

        self.objective_display = BonusObjectiveDisplay(self.current_objectives, self.SMALLER_FONT, self.screen)

        #super weapon sounds (start and stop reset)
        if hasattr(self.player, "beam_audio_playing") and self.player.beam_audio_playing:
            self.player.laser_beam_sound.stop()
            self.player.beam_audio_playing = False

        self.player.is_using_sw = False
        self.player.is_charging = False

        print("[DEBUG] Game state reset. Beam and sounds stopped.")

    # Update the current game state
    def update(self):
        self.ticks = pygame.time.get_ticks()
        self.delta_time = (self.ticks - self.ticks_last_frame) / 1000
        self.ticks_last_frame = self.ticks

        self.states[self.current_state].update(self)

    # Draw the current game state to the screen
    def draw(self):
        self.states[self.current_state].draw(self)
        pygame.display.flip()
