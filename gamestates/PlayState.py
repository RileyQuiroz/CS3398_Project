import pygame
import sys
import random
import time
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
from characters.enemies.enemy_spawn_and_despawn import *
from tools.collision_hanlder import check_projectile_enemy_collisions, check_player_projectile_collisions, check_player_consumable_collisions
from tools.Star_and_planet_bg_logic import Background, EvilBackground
from characters.player_char import Consumable, spawn_consumable
from obstacles import *

from tools.colors import Colors
from tools.sounds import Sounds
from gamestates.GameState import GameState

class PlayState(GameState):
    def __init__(self, game):
        super().__init__(game)

        # Initialize background
        self.background = Background(game.screen)

        # Containers and variables for enemies and projectiles
        self.to_despawn = pygame.sprite.Group()
        self.dest_enemies = []
        self.max_enemies = 3
        self.last_boss_location = [] # Used for boss defeat sequence

        self.save_text_show = False
        self.message = ""
        self.running = True
        self.black_bg = (0, 0, 0)

        self.start_time = 0.0

        self.spawn_tickets = 0
        self.last_spawn = 0
        self.last_spawn_wave = 0
        self.shots_fired = 0
        self.hits_detected = 0
       
        ##CONSUMABLE CREATION
        self.consumables_group = pygame.sprite.Group()
        self.consumable_spawn_timer = 0
        self.consumable_spawn_rate = 4000 # seconds between spawns CHANGE IF NEEDED
        self.max_consumables = 8

        self.level_progressed = False
        self.boss_spawned = False
        self.boss_defeated_time = 0

        #consumables_group.add(Consumable(200,100, "repair_kit"))
        #consumables_group.add(Consumable(120,120, "shield_pack"))

    def enter(self, game):
        if game.previous_state != 'pause':
            game.reset()
            self.__init__(game)

            self.max_enemies = 3 + game.difficulty
            self.spawn_tickets = 6 + game.difficulty

        # Play in-game background music
        pygame.mixer.music.load("assets/sound_efx/game_bg_music.mp3")  # Replace with your in-game music file
        pygame.mixer.music.set_volume(0.2)  # Adjust volume as needed
        pygame.mixer.music.play(-1)  # Play the music indefinitely (-1 for looping)

        game.timer.start()
        self.running = True

    def boss_transition_scene(self, game, old_background, new_background):
        fade_speed = 5  # Adjust to control fade speed
        font = pygame.font.Font("assets/fonts/Future Edge.ttf", 48)
        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/sound_efx/boss_music.mp3")
        pygame.mixer.music.play(-1)

        # Fade out the old background
        for alpha in range(0, 255, fade_speed):
            overlay = pygame.Surface((800, 600))  # Screen dimensions
            overlay.fill((0, 0, 0))  # Black overlay
            overlay.set_alpha(alpha)
            old_background.draw()  # Draw the current background
            game.screen.blit(overlay, (0, 0))  # Apply fade effect
            pygame.display.flip()
            pygame.time.delay(10)  # Adjust delay for smoother fade

        # Display the "Boss Incoming" message
        game.screen.fill((0, 0, 0))  # Black screen
        game.draw_text("", font, (255, 0, 0), 400, 300)  # Red text
        pygame.display.flip()
        pygame.time.delay(2000)  # Show message for 2 seconds

        # Fade in the new background
        for alpha in range(255, 0, -fade_speed):
            overlay = pygame.Surface((800, 600))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(alpha)
            new_background.draw()  # Draw the new background
            game.screen.blit(overlay, (0, 0))
            pygame.display.flip()
            pygame.time.delay(10)  # Adjust delay for smoother fade

    def update(self, game):
        self.background.update(game.timer)

        if self.running:
           game.timer.update(game.delta_time)

        #player weapon timer
        game.player.update_weapon_timer()

        if not game.timer.stopped and game.ticks - self.consumable_spawn_timer > self.consumable_spawn_rate:
            if len(self.consumables_group) < self.max_consumables:
                spawn_consumable(self.consumables_group, game.WIDTH, game.HEIGHT, is_boss_fight=(game.win_lose_system.current_level == 3))
                self.consumable_spawn_timer = game.ticks


        hit_detected = False

        if(game.win_lose_system.current_level == 3):
            check_projectile_boss_collisions(game.proj_group, game.enemy_group)
        else:
            hit_detected = check_projectile_enemy_collisions(game.proj_group, game.enemy_group)

        #print("hit detected: ", hit_detected)
        if hit_detected:
            self.hits_detected += 1 

        check_projectile_enemy_collisions(game.proj_group, game.enemy_group)
        check_player_projectile_collisions(game.player, game.enemy_projectiles, 10, game.timer.elapsed_time)
        check_player_consumable_collisions(game.player, self.consumables_group)

        game.proj_group.update(game.timer.stopped, game.proj_group, game.timer.elapsed_time)
        game.enemy_projectiles.update(game.timer.stopped, game.enemy_projectiles, game.timer.elapsed_time)

        game.player.handle_input(game.timer.stopped)

        for obstacle in game.obstacle_group:
            obstacle.update(game.player, game.delta_time)
            
        # Enemy Spawning
        self.last_spawn, self.last_spawn_wave, self.lvlThreeSwitch, self.spawn_tickets = levelSpawner(
            game.timer.elapsed_time,
            game.timer.stopped,
            game.enemy_group,
            self.max_enemies,
            self.last_spawn,
            self.last_spawn_wave,
            game.win_lose_system.current_level,
            game.lvlThreeSwitch,
            game.difficulty,
            self.spawn_tickets
        )

        if (game.win_lose_system.current_level == 3) and self.boss_spawned == False:
            # Create the new background for the boss level
            boss_background = EvilBackground(game.screen)

            # Perform the transition from the old background to the new boss background
            self.boss_transition_scene(game, self.background, boss_background)

            # Switch to the boss background
            self.background = boss_background
            self.level_progressed = True
            
            spawnBoss(game.enemy_group, 0, game.difficulty)
            self.boss_spawned = True

        # Update enemy conditions
        for enemy in game.enemy_group:
            startRetreat(enemy, self.to_despawn) # Enemy B retreat call
            # enemy.change_color() # Change color if hurt
            enemy.update(game.timer.stopped, game.timer.elapsed_time)
            enemy.fire_shot(game.enemy_projectiles, game.timer.stopped, game.timer.elapsed_time, game.player.x, game.player.y)
            check_player_enemy_physical_collision(game.player, enemy, game.timer.elapsed_time)

            if not enemy.living:
                destroyEnemy(self.dest_enemies, enemy, Sounds.ship_destroyed)

                if (enemy.size == 100):
                    game.timer.toggle()

                game.score_system.increase(10)
        
        # Check if a wave of enemies has finished
        wave_done = False

        if len(game.enemy_group) == 0 and game.win_lose_system.current_level not in game.win_lose_system.level_processed and game.timer.elapsed_time >= 5 and self.spawn_tickets <= 0:
            if game.timer.elapsed_time - game.win_lose_system.level_start_time >= game.level_cooldown:
                if game.win_lose_system.current_level != 3:
                    game.win_lose_system.update(game.timer.elapsed_time, game.current_objectives, wave_done=True)
                    wave_done = False
                    self.spawn_tickets = 6 + game.difficulty
                    if game.win_lose_system.current_level == 3:
                        self.spawn_tickets = 0
                    #if win_lose_system.current_level == 2:
                    #    level_cooldown = 10
                elif game.win_lose_system.current_level == 3:
                    game.win_lose_system.update(game.timer.elapsed_time, game.current_objectives, wave_done=True)
                    self.boss_defeated_time = time.time()
                    self.spawn_tickets = 0
                    wave_done = False
        else:
            game.win_lose_system.update(game.timer.elapsed_time, game.current_objectives, wave_done=False)
 
        # Check if the current level is still ongoing
        current_game_state = game.win_lose_system.update(game.timer.elapsed_time, game.current_objectives, wave_done=False)

        game.win_lose_system.render_overlay(game.screen)

        # If the current level is no longer ongoing, update the game state
        if current_game_state != WinLoseState.ONGOING:
            pygame.mixer.music.stop()
            # Stop beam sound and reset states
            if hasattr(game.player, "beam_audio_playing") and game.player.beam_audio_playing:
                game.player.laser_beam_sound.stop()
                game.player.beam_audio_playing = False
            game.player.is_using_sw = False
            game.player.is_charging = False
            print("[DEBUG] Game over. Beam and sounds stopped.")

            next_state = 'win' if current_game_state == WinLoseState.WIN else 'game_over'
            game.change_state(next_state)

        # AUTO TURRET STUFF
        keys = pygame.key.get_pressed()
        if game.player.player_weapon == "auto_turret" and keys[pygame.K_SPACE]:
            game.player.shoot(game.timer.stopped)
        elif game.player.player_weapon == "super_weapon":
            if keys[pygame.K_SPACE]:  # Start charging if space is pressed
                if not game.player.is_using_sw and not game.player.is_charging:
                    game.player.is_charging = True
                    game.player.charge_start_time = pygame.time.get_ticks()
                    game.player.laser_charge_sound.play()  # Play the charging sound
                    print("[DEBUG] Beam charging...")
                elif game.player.is_charging:  # Check if charging is complete
                    current_time = pygame.time.get_ticks()
                    if current_time - game.player.charge_start_time >= game.player.charge_duration:
                        game.player.is_charging = False
                        game.player.is_using_sw = True
                        game.player.laser_charge_sound.stop()  # Stop charging sound
                        if not hasattr(game.player, "beam_audio_playing") or not game.player.beam_audio_playing:
                            game.player.laser_beam_sound.play(-1)  # Play beam sound in a loop
                            game.player.beam_audio_playing = True
                        print("[DEBUG] Beam activated!")
            else:  # Deactivate the beam when space is released
                if game.player.is_using_sw or game.player.is_charging:
                    game.player.is_using_sw = False
                    game.player.is_charging = False
                    game.player.laser_charge_sound.stop()  # Stop charging sound

                    if hasattr(game.player, "beam_audio_playing") and game.player.beam_audio_playing:
                        game.player.laser_beam_sound.stop()  # Stop beam sound
                        game.player.beam_audio_playing = False
                    print("[DEBUG] Beam deactivated")

        # Handle beam damage
        if game.player.is_using_sw:
            check_beam_enemy_collisions(game.player, game.enemy_group, damage=8)
        
        # For accuracy bonus objective
        #self.shots_fired = 0

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
                    game.change_state('pause')
                elif event.key == pygame.K_p:
                    game.change_state('pause')
                elif event.key == pygame.K_SPACE:
                    game.player.shoot(game.timer.stopped)
                    self.shots_fired += 1
                # elif event.key == pygame.K_s:
                #     message, start_time = user_save_and_load.saveHandling(game.score_system.get_score(), game.player, game.win_lose_system.current_level, game.difficulty)
                #     self.save_text_show = True
                # elif event.key == pygame.K_l:
                #     game.reset()
                #     self.message, self.start_time, game.player.health, game.score_system.score, game.player.player_weapon, game.current_level, game.difficulty, game.player.shield, game.player.player_model, game.timer.elapsed_time = user_save_and_load.loadHandling(game.score_system.get_score(), game.timer.elapsed_time, game.player, game.current_level, game.difficulty)
                #     self.last_spawn = 0
                #     self.last_spawn_wave = 0
                #     self.save_text_show = True

        despawnEnemy(self.to_despawn)

        # Check if there were any collisions and record shots
        for _ in range(self.shots_fired):  # Loop through the number of shots fired
            if self.hits_detected >= 0:  # If there have been any successful hits
                game.win_lose_system.record_shot(hit=True)
                self.hits_detected -= 1  # Decrement hits to keep track
                #print(" MAIN LOOP SHOT DETECTED AS TRUE: Hits Left = ", hits_detected)
            else:  # If no hits were detected
                game.win_lose_system.record_shot(hit=False)
                #print(" MAIN LOOP SHOT DETECTED AS FALSE: Hits Left = ", hits_detected)

        game.clock.tick(game.FPS)
    
    def draw(self, game):
        self.background.draw()
        game.player.draw(game.screen, game.timer.elapsed_time)
        game.enemy_group.draw(game.screen)
        game.proj_group.draw(game.screen)
        game.enemy_projectiles.draw(game.screen)

        for enemy in game.enemy_group:
            enemy_health_bar = pygame.rect.Rect(
                enemy.rect.x,
                enemy.rect.y - 5,
                enemy.rect.width / enemy.max_health * enemy.health,
                3
            )

            pygame.draw.rect(game.screen, (100, 255, 100), enemy_health_bar)

        if (game.win_lose_system.current_level == 3):
            for enemy in game.enemy_group:
                enemy.boss_ui(game.screen)

        for obstacle in game.obstacle_group:
            obstacle.draw(game.screen)
     
        self.consumables_group.draw(game.screen)

        for dest_enemy in self.dest_enemies:
            enemy_center = dest_enemy[0]
            time_destroyed = dest_enemy[1]
            size = dest_enemy[2]

            if pygame.time.get_ticks() - time_destroyed <= 250:
                pygame.draw.circle(game.screen, (200, 180, 0), enemy_center, size)
            else:
                self.dest_enemies.remove(dest_enemy)

        if self.save_text_show:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time < 1500:
                game.draw_text(self.message, game.SMALLER_FONT, Colors.WHITE, game.WIDTH // 2, game.HEIGHT // 2 + 250)
            else:
                self.save_text_show = False

        game.win_lose_system.render_overlay(game.screen)
        game.objective_display.draw()
        game.draw_text(f"{game.timer.elapsed_time:.2f}", game.SMALL_FONT, Colors.NEON_CYAN, 100, 100)
        game.score_display.display_score(game.score_system.get_score())

    def leave(self, game):
        pygame.mixer.music.stop()
        #game.timer.stop()
        self.running = False

        if game.current_state != 'pause':
            #game.reset()
            game.set_obstacles()
            self.consumables_group.empty()
            self.consumable_spawn_timer = 0
