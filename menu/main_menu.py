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
from tools.collision_hanlder import check_projectile_enemy_collisions, check_player_projectile_collisions
from tools.Star_and_planet_bg_logic import Background
from characters.player_char import Consumable, spawn_consumable


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

def reset_game_state(player, score_system, timer, win_lose_system, proj_group, enemy_group, enemy_projectiles):
    score_system.reset()
    timer.reset()
    player.heal(100)
    player.is_alive = True
    win_lose_system.reset()
    proj_group.empty()
    enemy_group.empty()  # Clear all enemies
    enemy_projectiles.empty()
    timer.start()
    obstacle_group = set_obstacles()
    player.x = WIDTH // 2
    player.y = HEIGHT - 100

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

    last_spawn = 0
    last_spawn_wave = 0
    ticks_last_frame = pygame.time.get_ticks()
    
    #IMPORTANT: TEMP VARIABLEs FOR SAVE SYSTEM, USE/MODIFY FOR WHATEVER YOU NEED
    current_level = 3 # 0-2 are normal levels, 3 is boss
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
        

    while running:
        ##screen.fill(black_bg)
        background.update(timer)
        background.draw()

        ##DRAW CONSUMABLES
        consumables_group.draw(screen)

        ticks = pygame.time.get_ticks()
        delta_time = (ticks - ticks_last_frame) / 1000.0
        ticks_last_frame = ticks

        timer.update(delta_time)

        #SPAWN THE CONSUMABLES
        max_consumables = 10
        if not timer.stopped and ticks - consumable_spawn_timer > consumable_spawn_rate:
            if len(consumables_group) < max_consumables:
                spawn_consumable(consumables_group, WIDTH, HEIGHT)
                consumable_spawn_timer = ticks

        if(current_level == 3):
            check_projectile_boss_collisions(proj_group, enemy_group, damage=1)
        else:
            check_projectile_enemy_collisions(proj_group, enemy_group, damage=1)
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
        
        current_game_state = win_lose_system.update()

        ## Check win/loss condition and then go to end screen
        if current_game_state != GameState.ONGOING:
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
                        if consumable.consumable_type in ["auto_turret", "plasma_gun", "rocket_launcher"]:
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

        # Destruction animations
        for enemy_center, time_destroyed, size, isBoss in dest_enemies[:]:
            explosion_durration = pygame.time.get_ticks() - time_destroyed
            # Boss destruction sequence
            if isBoss == 1 and explosion_durration <= 3750:
                # Draw destroyed boss
                if explosion_durration <= 3600:
                    center_size = 75
                    wing_size_x = 75
                    wing_size_y = 20
                    boss_color = (255,140,0)
                    square_rect = pygame.Rect(enemy_center[0] - center_size // 2, enemy_center[1] - center_size // 2, center_size, center_size)
                    pygame.draw.rect(screen, boss_color, square_rect)
                    left_rect = pygame.Rect(enemy_center[0] - center_size // 2 - wing_size_x, enemy_center[1] - wing_size_y // 2, wing_size_x, wing_size_y)
                    pygame.draw.rect(screen, boss_color, left_rect)
                    right_rect = pygame.Rect(enemy_center[0] + center_size // 2, enemy_center[1] - wing_size_y // 2, wing_size_x, wing_size_y)
                    pygame.draw.rect(screen, boss_color, right_rect)
                # Boss explosions
                if explosion_durration <= 1200:
                    wing_center = (enemy_center[0] + 75, enemy_center[1])
                    pygame.draw.circle(screen, (200, 180, 0), wing_center, size/2)
                    if explosion_durration == 0:
                        ship_destroyed_sound.play()
                elif explosion_durration <= 2400:
                    wing_center = (enemy_center[0] - 75, enemy_center[1])
                    pygame.draw.circle(screen, (200, 180, 0), wing_center, size/2)
                    if explosion_durration <= 1215:
                        ship_destroyed_sound.play()
                elif explosion_durration <= 3600:
                    pygame.draw.circle(screen, (200, 180, 0), enemy_center, size*1.3)
                    if explosion_durration <= 2415:
                        ship_destroyed_sound.play()
            elif isBoss != 1 and explosion_durration <= 250:
                pygame.draw.circle(screen, (200, 180, 0), enemy_center, size)
            else:
                if(isBoss == 1):
                    score_system.increase(990) # Get more points for destroying boss
                dest_enemies.remove((enemy_center, time_destroyed, size, isBoss))
                

        despawnEnemy(to_despawn)
        pygame.display.flip()
        clock.tick(FPS)
