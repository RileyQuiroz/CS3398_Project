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
from characters.enemies.enemy_spawn_and_despawn import *
from tools.collision_hanlder import (
    check_player_projectile_collisions,
    check_projectile_enemy_collisions,
    check_player_consumable_collisions 
)
from tools.Star_and_planet_bg_logic import Background
from characters.player_char import Consumable, spawn_consumable
from tools.bonus_objectives import BonusObjective, NoDamageObjective, AccuracyObjective, UnderTimeObjective, KillStreakObjective, BonusObjectiveDisplay


# Initialize pygame and mixer for sound
pygame.init()
pygame.mixer.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BULLETHELL")

# Load background
background = pygame.image.load("assets/backgrounds/space_background4.png")  # Load your space background image
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Define colors
NEON_CYAN = (0, 255, 255)
NEON_PURPLE = (155, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define leaderboard for fastest finishing times
leaderboard = Leaderboard("time_scoreboard.json")

############# FONT AND TEXT ALIGNTMENT #########################
# Load a futuristic font (if you have one)
font = pygame.font.Font("assets/fonts/Future Edge.ttf", 74)
# Smaller font for choices in other menus (records and settings)
smaller_font = pygame.font.Font("assets/fonts/Future Edge.ttf", 34)
def draw_text_left_aligned(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(topleft=(x, y))  # Align to the left (top-left corner)
    surface.blit(text_obj, text_rect)
    return text_rect


###################################################################

# Load hover sound
hover_sound = pygame.mixer.Sound("assets/sound_efx/hover_sound.wav")  # Replace with your sound file

# Enemy sounds
ship_destroyed_sound = pygame.mixer.Sound("assets/sound_efx/enemy_down.wav")
ship_destroyed_sound.set_volume(.35)
enemy_shot_sound = pygame.mixer.Sound("assets/sound_efx/enemy_shot.wav")
enemy_shot_sound.set_volume(.2)
enemy_hurt_sound = pygame.mixer.Sound("assets/sound_efx/enemy_hurt.wav")
enemy_hurt_sound.set_volume(.15)

# Define framerate, clock, and in-game timer
FPS = 60
clock = pygame.time.Clock()
timer = Timer()
timer.start()

# Initialize Score and ScoreDisplay
score_system = Score()
score_display = ScoreDisplay(screen, font_size=36, color=NEON_CYAN, position=(50, 50))

# Win/Lose System to update game state
win_lose_system = WinLoseSystem(score_system, player=None) ##player set after instantiation



# Define in-game obstacles
BOULDER_PATH = "assets/objects/spr_boulder_0.png"

def set_obstacles():
    return [
        Mover((200, 200), (10, 10), BOULDER_PATH),
        Rotator((200, 400), BOULDER_PATH),
        ZigZag((0, 300), (50, 0), BOULDER_PATH),
        Dangerous((500, 550), BOULDER_PATH),
        Destructible((550, 300), 5, BOULDER_PATH),
        Friend((100, 200), 5, score_system, BOULDER_PATH)
    ]

obstacle_group = set_obstacles()

# Define menu options
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)
    return text_rect

def main_menu():
    current_menu = 'main'  # Track the current menu ('main', 'settings', 'records')

    # Track hover states for each menu option
    hovered = {
        'start_game': False,
        'records': False,
        'settings': False,
        'quit': False,
        'back': False  # Hover state for the 'Back' option in other menus
    }

    while True:
        screen.blit(background, (0, 0))  # Draw the background
        #background.update()
        #background.draw()
        mouse_pos = pygame.mouse.get_pos()

        # Handle the main menu
        if current_menu == 'main':
            # Check if mouse is hovering over the options and set color accordingly
            start_color = NEON_PURPLE if hovered['start_game'] else WHITE
            records_color = NEON_PURPLE if hovered['records'] else WHITE
            settings_color = NEON_PURPLE if hovered['settings'] else WHITE
            quit_color = NEON_PURPLE if hovered['quit'] else WHITE

            # Draw main menu options with updated hover colors
            start_game_rect = draw_text('Start Game', font, start_color, screen, WIDTH // 2, HEIGHT // 2 - 150)
            records_rect = draw_text('Records', font, records_color, screen, WIDTH // 2, HEIGHT // 2 - 50)
            settings_rect = draw_text('Settings', font, settings_color, screen, WIDTH // 2, HEIGHT // 2 + 50)
            quit_rect = draw_text('Quit', font, quit_color, screen, WIDTH // 2, HEIGHT // 2 + 150)

            # Hover and sound logic for the main menu
            if start_game_rect.collidepoint(mouse_pos):
                if not hovered['start_game']:
                    hover_sound.play()
                    hovered['start_game'] = True
            else:
                hovered['start_game'] = False

            if records_rect.collidepoint(mouse_pos):
                if not hovered['records']:
                    hover_sound.play()
                    hovered['records'] = True
            else:
                hovered['records'] = False

            if settings_rect.collidepoint(mouse_pos):
                if not hovered['settings']:
                    hover_sound.play()
                    hovered['settings'] = True
            else:
                hovered['settings'] = False

            if quit_rect.collidepoint(mouse_pos):
                if not hovered['quit']:
                    hover_sound.play()
                    hovered['quit'] = True
            else:
                hovered['quit'] = False

        # Handle the records menu
        elif current_menu == 'records':
            # Display a simple "Records" title and "Back" option
            draw_text('Records', font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 250)

            # Display fastest finishing times
            for i in range(len(leaderboard.high_scores)):
                rank = str(i + 1) + '.'
                initials = str(leaderboard.high_scores[i][0])
                score = str(leaderboard.high_scores[i][1])
                entry = rank + "\t" + initials + "\t" + score
                
                # Draw the leaderboard entry
                draw_text(entry, font, WHITE, screen, WIDTH // 2, HEIGHT // 3.5 + (80 * i))

            back_color = NEON_PURPLE if hovered['back'] else WHITE
            back_rect = draw_text('Back', font, back_color, screen, WIDTH // 2, HEIGHT // 2 + 250)

            if back_rect.collidepoint(mouse_pos):
                if not hovered['back']:
                    hover_sound.play()
                    hovered['back'] = True
            else:
                hovered['back'] = False

        # Handle the settings menu
        elif current_menu == 'settings':
            # Display a simple "Settings" title and "Back" option
            draw_text('Settings', font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 250)
            draw_text_left_aligned('Difficulty', smaller_font, WHITE, screen, 50, HEIGHT // 2 - 50)
            back_color = NEON_PURPLE if hovered['back'] else WHITE
            back_rect = draw_text('Back', font, back_color, screen, WIDTH // 2, HEIGHT // 2 + 150)

            if back_rect.collidepoint(mouse_pos):
                if not hovered['back']:
                    hover_sound.play()
                    hovered['back'] = True
            else:
                hovered['back'] = False

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_menu == 'main':
                    # Check which option is clicked and switch to the respective menu
                    if start_game_rect.collidepoint(event.pos):
                        print("Start Game clicked!")
                        obstacle_group = set_obstacles()
                        timer.reset()  # Reset timer when starting a new game
                        timer.start()  # Start the timer
                        game_loop()  # Switch to the game loop
                    elif records_rect.collidepoint(event.pos):
                        current_menu = 'records'  # Switch to Records menu
                    elif settings_rect.collidepoint(event.pos):
                        current_menu = 'settings'  # Switch to Settings menu
                    elif quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

                elif current_menu in ['records', 'settings']:
                    # Handle "Back" button in Records or Settings
                    if back_rect.collidepoint(event.pos):
                        current_menu = 'main'  # Switch back to Main menu

        # Update the display
        pygame.display.update()

# Once game states is finalized, split game_loop functions into different sections depending on game state
# Define the display_defeat_message function
def display_defeat_message(screen, font):
    screen.fill((0, 0, 0))  # Fill screen with black
    defeat_text = font.render("Defeated", True, (255, 0, 0))  # Red text for defeated message
    text_rect = defeat_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(defeat_text, text_rect)
    obstacle_group = set_obstacles()
    pygame.display.flip()  # Update the display

def assign_bonus_objectives():
    """
    Randomly select two bonus objectives from the pool.
    """
    objectives_pool = [
        NoDamageObjective(),
        UnderTimeObjective(),
        AccuracyObjective(),
    ]
    return random.sample(objectives_pool, 2)


def reset_game_state(player, score_system, timer, win_lose_system, proj_group, enemy_group, enemy_projectiles):
    score_system.reset()
    timer.reset()
    player.heal(100)
    player.is_alive = True
    player.player_weapon = "default"
    win_lose_system.reset()
    proj_group.empty()
    enemy_group.empty()  # Clear all enemies
    enemy_projectiles.empty()
    timer.start()
    obstacle_group = set_obstacles()
    player.x = WIDTH // 2
    player.y = HEIGHT - 100

    #super weapon sounds (start and stop reset)
    if hasattr(player, "beam_audio_playing") and player.beam_audio_playing:
        player.laser_beam_sound.stop()
        player.beam_audio_playing = False
    player.is_using_sw = False
    player.is_charging = False
    print("[DEBUG] Game state reset. Beam and sounds stopped.")

def game_loop():
    small_font = pygame.font.Font("assets/fonts/Future Edge.ttf", 32)
    #init background
    background = Background(screen)

    # Containers and variables for enemies and projectiles
    enemy_group = pygame.sprite.Group()
    proj_group = pygame.sprite.Group()
    enemy_projectiles = pygame.sprite.Group()
    to_despawn = pygame.sprite.Group()
    dest_enemies = []
    max_enemies = 3
    last_boss_location = [] # used for boss defeat sequence

    obstacle_group = set_obstacles()

    save_text_show = False
    message = ""
    start_time = 0
    running = True
    black_bg = (0, 0, 0)
    timer.reset()
    timer.start()

    player = CharacterPawn(x=WIDTH // 2, y=HEIGHT - 100, projectiles_group=proj_group, screen_width=WIDTH, screen_height=HEIGHT)
    win_lose_system.player = player
    win_lose_system.player_tracker.player = player

    last_spawn = 0
    last_spawn_wave = 0
    ticks_last_frame = pygame.time.get_ticks()
    
    #IMPORTANT: TEMP VARIABLEs FOR SAVE SYSTEM, USE/MODIFY FOR WHATEVER YOU NEED
    current_level = 1 # 0-2 are normal levels, 3 is boss
    lvlThreeSwitch = 0 # Used only for level 3 spawning of type c and b
    difficulty = 0 # 0-easy, 1-medium, 2-hard
    
    max_enemies = 3 + difficulty # Assumes 3 difficulties, easy(0), medium(1), hard(2)

    ##CONSUMABLE CREATION
    consumables_group = pygame.sprite.Group()
    consumable_spawn_timer = 0
    consumable_spawn_rate = 5000 # seconds between spawns CHANGE IF NEEDED
    #consumables_group.add(Consumable(200,100, "repair_kit"))
    #consumables_group.add(Consumable(120,120, "shield_pack"))
    
    if(current_level == 3):
        spawnBoss(enemy_group, 0, difficulty)
        

    #current_level = 1
    level_progressed = False

    # Assign and initialize objectives
    current_objectives = assign_bonus_objectives()
    for obj in current_objectives:
        obj.initialize(player, win_lose_system) # FIXME: current_level being passed isn't right or works

    # Display objectives
    print("Bonus Objectives for this level:")
    for obj in current_objectives:
        print(f"- {obj.description}")

    hits_detected = 0

    objective_display = BonusObjectiveDisplay(current_objectives, font, screen)

    while running:
        keys = pygame.key.get_pressed()

        if player.player_weapon == "super_weapon":
            if keys[pygame.K_SPACE]:  # Start charging if space is pressed
                if not player.is_using_sw and not player.is_charging:
                    player.is_charging = True
                    player.charge_start_time = pygame.time.get_ticks()
                    player.laser_charge_sound.play()  # Play the charging sound
                    print("[DEBUG] Beam charging...")

                elif player.is_charging:  # Check if charging is complete
                    current_time = pygame.time.get_ticks()
                    if current_time - player.charge_start_time >= player.charge_duration:
                        player.is_charging = False
                        player.is_using_sw = True
                        player.laser_charge_sound.stop()  # Stop charging sound
                        if not hasattr(player, "beam_audio_playing") or not player.beam_audio_playing:
                            player.laser_beam_sound.play(-1)  # Play beam sound in a loop
                            player.beam_audio_playing = True
                        print("[DEBUG] Beam activated!")

            else:  # Deactivate the beam when space is released
                if player.is_using_sw or player.is_charging:
                    player.is_using_sw = False
                    player.is_charging = False
                    player.laser_charge_sound.stop()  # Stop charging sound
                    if hasattr(player, "beam_audio_playing") and player.beam_audio_playing:
                        player.laser_beam_sound.stop()  # Stop beam sound
                        player.beam_audio_playing = False
                    print("[DEBUG] Beam deactivated")

        # Handle beam damage
        if player.is_using_sw:
            check_beam_enemy_collisions(player, enemy_group, damage=8)

        # For accuracy bonus objective
        shots_fired = 0

        ##screen.fill(black_bg)
        background.update(timer)
        background.draw()

        ##DRAW CONSUMABLES
        consumables_group.draw(screen)

        ticks = pygame.time.get_ticks()
        delta_time = (ticks - ticks_last_frame) / 1000.0
        ticks_last_frame = ticks

        timer.update(delta_time)

        # FIXME TODO: Testing, might not work: *OBJECTIVE DISPLAY*
        objective_display.draw()

        #SPAWN THE CONSUMABLES
        max_consumables = 10
        if not timer.stopped and ticks - consumable_spawn_timer > consumable_spawn_rate:
            if len(consumables_group) < max_consumables:
                spawn_consumable(consumables_group, WIDTH, HEIGHT)
                consumable_spawn_timer = ticks

        if(current_level == 3):
            check_projectile_boss_collisions(proj_group, enemy_group)
        else:
            hit_detected = check_projectile_enemy_collisions(proj_group, enemy_group)


        #print("hit detected: ", hit_detected)
        if hit_detected == True:
            hits_detected += 1 


        # Call to check collisions with player projectiles
        check_player_projectile_collisions(player, enemy_projectiles, 10, timer.elapsed_time)

        # Always check for player-consumable collisions

        check_player_consumable_collisions(player, consumables_group)

        # Check for player-projectile collisions
        check_player_projectile_collisions(player, enemy_projectiles, 10, timer.elapsed_time)


        proj_group.update(timer.stopped, proj_group, timer.elapsed_time)
        enemy_projectiles.update(timer.stopped, enemy_projectiles, timer.elapsed_time)

        player.handle_input(timer.stopped)
        player.draw(screen, timer.elapsed_time)
        proj_group.draw(screen)
        enemy_projectiles.draw(screen)

        for obstacle in obstacle_group:
            obstacle.update(player, delta_time)
            obstacle.draw(screen)
            
        # Enemy Spawning
        last_spawn, last_spawn_wave, lvlThreeSwitch = levelSpawner(timer.elapsed_time, timer.stopped, enemy_group, max_enemies, last_spawn, last_spawn_wave, current_level, lvlThreeSwitch, difficulty)
        #last_spawn, last_spawn_wave = oldSpawner(timer.elapsed_time, timer.stopped, enemy_group, max_enemies, last_spawn, last_spawn_wave)           

        # Update enemy conditions
        for enemy in enemy_group:
            startRetreat(enemy, to_despawn) # Enemy B retreat call
            enemy.change_color() # Change color if hurt
            enemy.update(timer.stopped, timer.elapsed_time)
            enemy.fire_shot(enemy_projectiles, timer.stopped, timer.elapsed_time, player.x, player.y)
            check_player_enemy_physical_collision(player, enemy, timer.elapsed_time)
            if not enemy.living:
                destroyEnemy(dest_enemies, enemy, ship_destroyed_sound)
                if(enemy.size == 100): # Only boss has size 100
                    timer.toggle()
                score_system.increase(10)
        enemy_group.draw(screen)

        draw_text(f"{timer.elapsed_time:.2f}", small_font, NEON_CYAN, screen, 100, 100)
        score_display.display_score(score_system.get_score())
        
        win_lose_system.update(timer.elapsed_time, current_objectives)
        current_game_state = win_lose_system.update(timer.elapsed_time, current_objectives)
        win_lose_system.render_overlay(screen)

        ##if win_lose_system.current_level == 2 and level_progressed == False:
        ##    current_objectives = assign_bonus_objectives()
        ##    level_progressed = True
        ##    print("Bonus Objectives for this level:")
        ##    for obj in current_objectives:
        ##        print(f"- {obj.description}")

        if current_game_state != GameState.ONGOING:
            # Stop beam sound and reset states
            if hasattr(player, "beam_audio_playing") and player.beam_audio_playing:
                player.laser_beam_sound.stop()
                player.beam_audio_playing = False
            player.is_using_sw = False
            player.is_charging = False
            print("[DEBUG] Game over. Beam and sounds stopped.")

            ## Check win/loss condition and then go to end screen
            if(current_level != 3):
                end_screen = EndScreen(screen, player)
                end_screen_display = True
                while end_screen_display:
                    end_screen.display(current_game_state)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:  # Left mouse button
                                pos = event.pos
                                selected_option = end_screen.check_option_click(pos)
                                if selected_option == "Restart":
                                    end_screen_display = False
                                    reset_game_state(player, score_system, timer, win_lose_system, proj_group, enemy_group, enemy_projectiles)
                                    game_loop()
                                elif selected_option == "Main Menu":
                                    end_screen_display = False
                                    reset_game_state(player, score_system, timer, win_lose_system, proj_group, enemy_group, enemy_projectiles)
                                    main_menu()
                                elif selected_option == "Quit":
                                    pygame.quit()
                                    exit()
            elif(current_level == 3 and len(dest_enemies) == 0): # For boss destruction
                end_screen = EndScreen(screen, player)
                end_screen_display = True
                while end_screen_display:
                    end_screen.display(current_game_state)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:  # Left mouse button
                                pos = event.pos
                                selected_option = end_screen.check_option_click(pos)
                                if selected_option == "Restart":
                                    end_screen_display = False
                                    reset_game_state(player, score_system, timer, win_lose_system, proj_group, enemy_group, enemy_projectiles)
                                    game_loop()
                                elif selected_option == "Main Menu":
                                    end_screen_display = False
                                    reset_game_state(player, score_system, timer, win_lose_system, proj_group, enemy_group, enemy_projectiles)
                                    main_menu()
                                elif selected_option == "Quit":
                                    pygame.quit()
                                    exit()
        # AUTO TURRET STUFF
        keys = pygame.key.get_pressed()
        if player.player_weapon == "auto_turret" and keys[pygame.K_SPACE]:
         player.shoot(timer.stopped)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h: #THIS IS FOR TESTING##################
                    for consumable in consumables_group:
                        if consumable.consumable_type == "repair_kit":
                            current_health = player.health
                            player.consume(consumable.consumable_type)
                            # despawn consumable only if the shield increases
                            if player.health > current_health:
                                consumables_group.remove(consumable)
                                print("health kit activated")
                            break
                elif event.key == pygame.K_n: #THIS IS FOR TESTING#################
                    for consumable in consumables_group:
                        if consumable.consumable_type == "shield_pack":
                            current_shield = player.shield
                            player.consume(consumable.consumable_type)
                            if player.shield > current_shield:
                                consumables_group.remove(consumable)
                                print("shield pack consumed")
                            break
                elif event.key == pygame.K_c:
                    for consumable in consumables_group:
                        if consumable.consumable_type in ["auto_turret", "plasma_gun", "rocket_launcher", "super_weapon" ]:
                            player.consume(consumable.consumable_type)
                            consumables_group.remove(consumable)  # Remove the consumed item
                            print(f"Weapon switched to: {player.player_weapon}")
                            break
                if event.key == pygame.K_ESCAPE:
                    running = False
                    timer.stop()
                elif event.key == pygame.K_p:
                    timer.toggle()
                elif event.key == pygame.K_SPACE:
                    player.shoot(timer.stopped)
                    shots_fired += 1

                    # # Check if there were any collisions and record shots
                    #if hit_detected == True:  # If a hit was detected, shots hit the target
                    #    win_lose_system.record_shot(hit=True)
                    #    print(" MAIN LOOP SHOT DETECTED AS TRUE: ", hit_detected)
                    #elif hit_detected == False:  # No collisions, so the shots missed
                    #    win_lose_system.record_shot(hit=False)
                    #    print(" MAIN LOOP SHOT DETECTED AS false: ", hit_detected)

                elif event.key == pygame.K_s:
                    message, start_time = user_save_and_load.saveHandling(score_system.get_score(), player, current_level, difficulty)
                    save_text_show = True
                elif event.key == pygame.K_l:
                    reset_game_state(player, score_system, timer, win_lose_system, proj_group, enemy_group, enemy_projectiles)
                    message, start_time, player.health, score_system.score, player.player_weapon, current_level, difficulty, player.shield, player.player_model, timer.elapsed_time = user_save_and_load.loadHandling(score_system.get_score(), timer.elapsed_time, player, current_level, difficulty)
                    last_spawn = 0
                    last_spawn_wave = 0
                    save_text_show = True

        if save_text_show:
            current_time = pygame.time.get_ticks()
            if current_time - start_time < 1500:
                draw_text(message, smaller_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 250)
            else:
                save_text_show = False

        # Handle enemy destruction
        drawEnemyDestruction(dest_enemies, screen, ship_destroyed_sound, score_system)                
        despawnEnemy(to_despawn)

        # Check if there were any collisions and record shots
        for _ in range(shots_fired):  # Loop through the number of shots fired
            if hits_detected >= 0:  # If there have been any successful hits
                win_lose_system.record_shot(hit=True)
                hits_detected -= 1  # Decrement hits to keep track
                #print(" MAIN LOOP SHOT DETECTED AS TRUE: Hits Left = ", hits_detected)
            else:  # If no hits were detected
                win_lose_system.record_shot(hit=False)
                #print(" MAIN LOOP SHOT DETECTED AS FALSE: Hits Left = ", hits_detected)


        shots_fired = 0

        pygame.display.flip()
        clock.tick(FPS)
