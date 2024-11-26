import pygame
import sys
import random
from tools.timer import Timer
from tools.score_counter import Score
from tools.score_display import ScoreDisplay
from tools.collision_hanlder import *
from tools.game_states import GameState as WinLoseState
from tools.end_screen import EndScreen
from tools.win_lose_system import WinLoseSystem
from savesystem.leaderboard import Leaderboard
from savesystem import user_save_and_load
from characters.player_char import CharacterPawn
from characters.enemies.enemy_spawn_and_despawn import spawnEnemy, despawnEnemy, startRetreat, destroyEnemy
from tools.collision_hanlder import check_projectile_enemy_collisions, check_player_projectile_collisions
from tools.Star_and_planet_bg_logic import Background
from characters.player_char import Consumable, spawn_consumable
from obstacles import *

from tools.colors import Colors
from tools.sounds import Sounds
from gamestates.GameState import GameState

class PlayState(GameState):
    def __init__(self, game):
        super().__init__(game)

        #init background
        self.background = Background(game.screen)

        # Containers and variables for enemies and projectiles
        self.to_despawn = pygame.sprite.Group()
        self.dest_enemies = []
        self.max_enemies = 3

        self.save_text_show = False
        self.message = ""
        self.start_time = 0
        self.running = True
        self.black_bg = (0, 0, 0)

        self.last_spawn = 0
        self.last_spawn_wave = 0

        self.ticks = pygame.time.get_ticks()
        self.ticks_last_frame = 0.0
        self.delta_time = 0.0
        
        ##CONSUMABLE CREATION
        self.consumables_group = pygame.sprite.Group()
        self.consumable_spawn_timer = 0
        self.consumable_spawn_rate = 5000 # seconds between spawns CHANGE IF NEEDED
        self.max_consumables = 10
        #consumables_group.add(Consumable(200,100, "repair_kit"))
        #consumables_group.add(Consumable(120,120, "shield_pack"))

    def enter(self, game):
        if game.previous_state != 'pause':
            game.reset()
            spawnEnemy(game.enemy_group, game.timer.elapsed_time, 2) # Spawned in for testing

        game.timer.start()

    def update(self, game):
        self.background.update(game.timer)

        if self.running:
            self.ticks = pygame.time.get_ticks()
            self.delta_time = (self.ticks - self.ticks_last_frame) / 1000.0
            self.ticks_last_frame = self.ticks

            game.timer.update(self.delta_time)

        if not game.timer.stopped and self.ticks - self.consumable_spawn_timer > self.consumable_spawn_rate:
            if len(self.consumables_group) < self.max_consumables:
                spawn_consumable(self.consumables_group, game.WIDTH, game.HEIGHT)
                self.consumable_spawn_timer = self.ticks

        check_projectile_enemy_collisions(game.proj_group, game.enemy_group)
        check_player_projectile_collisions(game.player, game.enemy_projectiles, 10, game.timer.elapsed_time)

        game.proj_group.update(game.timer.stopped, game.proj_group, game.timer.elapsed_time)
        game.enemy_projectiles.update(game.timer.stopped, game.enemy_projectiles, game.timer.elapsed_time)

        game.player.handle_input(game.timer.stopped)
        game.proj_group.draw(game.screen)
        game.enemy_projectiles.draw(game.screen)

        for obstacle in game.obstacle_group:
            obstacle.update(game.player, self.delta_time)
            
        # Enemy Spawning
        if not game.timer.stopped and len(game.enemy_group) < self.max_enemies and game.timer.elapsed_time - self.last_spawn >= 4:
            spawnEnemy(game.enemy_group, game.timer.elapsed_time, 0)
            last_spawn = game.timer.elapsed_time
        if not game.timer.stopped and game.timer.elapsed_time - self.last_spawn_wave >= 30: #Spawn wave is not blocked by max enemies, set to 30s for demoing(ideally would be longer)
            spawnEnemy(game.enemy_group, game.timer.elapsed_time, 1)
            spawnEnemy(game.enemy_group, game.timer.elapsed_time, 0)
            spawnEnemy(game.enemy_group, game.timer.elapsed_time, 0)
            last_spawn_wave = game.timer.elapsed_time            

        # Update enemy conditions
        for enemy in game.enemy_group:
            startRetreat(enemy, self.to_despawn) # Enemy B retreat call
            enemy.change_color() # Change color if hurt
            enemy.update(game.timer.stopped, game.timer.elapsed_time)
            enemy.fire_shot(game.enemy_projectiles, paused=game.timer.stopped, curr=game.timer.elapsed_time, empty1=game.player.x, empty2=game.player.y)
            check_player_enemy_physical_collision(game.player, enemy, game.timer.elapsed_time)
            if not enemy.living:
                destroyEnemy(self.dest_enemies, enemy, Sounds.ship_destroyed)
                game.score_system.increase(10)

        game.enemy_group.draw(game.screen)

        game.draw_text(f"{game.timer.elapsed_time:.2f}", game.SMALL_FONT, Colors.NEON_CYAN, 100, 100)
        game.score_display.display_score(game.score_system.get_score())

        # Check if the current level is still ongoing
        current_game_state = game.win_lose_system.update(game.timer.elapsed_time, game.current_objectives)

        # If the current level is no longer ongoing, update the game state
        if current_game_state != WinLoseState.ONGOING:
            # end_screen = EndScreen(game.screen, game.player)
            next_state = 'win' if current_game_state == WinLoseState.WIN else 'game_over'
            game.change_state(next_state)

        # AUTO TURRET STUFF
        keys = pygame.key.get_pressed()
        if game.player.player_weapon == "auto_turret" and keys[pygame.K_SPACE]:
            game.player.shoot(game.timer.stopped)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h: #THIS IS FOR TESTING##################
                    for consumable in self.consumables_group:
                        if consumable.consumable_type == "repair_kit":
                            current_health = game.player.health
                            game.player.consume(consumable.consumable_type)
                            # despawn consumable only if the shield increases
                            if game.player.health > current_health:
                                self.consumables_group.remove(consumable)
                                print("health kit activated")
                            break
                elif event.key == pygame.K_n: #THIS IS FOR TESTING#################
                    for consumable in self.consumables_group:
                        if consumable.consumable_type == "shield_pack":
                            current_shield = game.player.shield
                            game.player.consume(consumable.consumable_type)
                            if game.player.shield > current_shield:
                                self.consumables_group.remove(consumable)
                                print("shield pack consumed")
                            break
                elif event.key == pygame.K_c:
                    for consumable in self.consumables_group:
                        if consumable.consumable_type in ["auto_turret", "plasma_gun", "rocket_launcher"]:
                            game.player.consume(consumable.consumable_type)
                            self.consumables_group.remove(consumable)  # Remove the consumed item
                            print(f"Weapon switched to: {game.player.player_weapon}")
                            break
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    game.change_state('pause')
                    # game.timer.stop()
                elif event.key == pygame.K_p:
                    self.running = False
                    game.change_state('pause')
                    #game.timer.toggle()
                elif event.key == pygame.K_SPACE:
                    game.player.shoot(game.timer.stopped)
                elif event.key == pygame.K_s:
                    message, start_time = user_save_and_load.saveHandling(game.score_system.get_score(), game.player, game.current_level, game.difficulty)
                    self.save_text_show = True
                elif event.key == pygame.K_l:
                    game.reset()
                    self.message, self.start_time, game.player.health, game.score_system.score, game.player.player_weapon, game.current_level, game.difficulty, game.player.shield, game.player.player_model, game.timer.elapsed_time = user_save_and_load.loadHandling(game.score_system.get_score(), game.timer.elapsed_time, game.player, game.current_level, game.difficulty)
                    self.last_spawn = 0
                    self.last_spawn_wave = 0
                    self.save_text_show = True

        if self.save_text_show:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time < 1500:
                game.draw_text(self.message, game.SMALLER_FONT, Colors.WHITE, game.WIDTH // 2, game.HEIGHT // 2 + 250)
            else:
                self.save_text_show = False

        #for enemy_center, time_destroyed, size in self.dest_enemies[:]:
        #    if pygame.time.get_ticks() - time_destroyed <= 250:
        #        pygame.draw.circle(game.screen, (200, 180, 0), enemy_center, size)
        #    else:
        #        self.dest_enemies.remove((enemy_center, time_destroyed, size))

        despawnEnemy(self.to_despawn)
        game.clock.tick(game.FPS)
    
    def draw(self, game):
        self.background.draw()
        game.player.draw(game.screen, game.timer.elapsed_time)
        game.enemy_group.draw(game.screen)
        game.proj_group.draw(game.screen)
        game.enemy_projectiles.draw(game.screen)
        
        for obstacle in game.obstacle_group:
            obstacle.draw(game.screen)
     
        self.consumables_group.draw(game.screen)

    def leave(self, game):
        game.timer.stop()

        if game.current_state != 'pause':
            game.timer.reset()
            game.proj_group.empty()
            game.enemy_group.empty()
            game.enemy_projectiles.empty()
            game.set_obstacles()
            self.consumables_group.empty()
            self.consumable_spawn_timer = 0
