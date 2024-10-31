import pygame
import sys
import random
from tools.timer import Timer
from tools.score_counter import Score
from tools.score_display import ScoreDisplay
from savesystem.leaderboard import Leaderboard
from savesystem import user_save_and_load
from characters.enemies.enemy_type_a import EnemyTypeA
from obstacles.Mover import Mover
from obstacles.Rotator import Rotator
from obstacles.ZigZag import ZigZag
from tools.game_states import GameState
from tools.win_lose_system import WinLoseSystem
from characters.enemies.enemy_spawn_and_despawn import spawnEnemy
from characters.player_char import CharacterPawn
from characters.enemies.enemy_spawn_and_despawn import spawnEnemy, despawnEnemy, startRetreat, destroyEnemy
from tools.collision_hanlder import check_projectile_enemy_collisions, check_player_projectile_collisions

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

# Define in-game obstacles
obstacle_group = [
    Mover(30, (200, 200), (10, 10), WHITE),
    Rotator(30, (200, 400), NEON_PURPLE),
    ZigZag(30, (0, 300), (50, 0), NEON_CYAN)
]

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
                        score_system.increase(10)  # For testing purposes
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
def game_loop():
    small_font = pygame.font.Font("assets/fonts/Future Edge.ttf", 32)
    # Containers and variables for enemies and projectiles
    enemy_group = pygame.sprite.Group()
    proj_group = pygame.sprite.Group()  # Player's projectiles
    enemy_projectiles = pygame.sprite.Group()  # Enemy projectiles
    to_despawn = pygame.sprite.Group()  # For despawning non-destroyed enemies
    dest_enemies = []  # For after-effects of enemy destruction
    max_enemies = 5  # Can be adjusted based on difficulty

    # Timer and score systems
    save_text_show = False
    message = ""
    start_time = 0
    running = True
    black_bg = (0, 0, 0)
    timer = Timer()
    timer.start()

    # Initialize player instance
    player = CharacterPawn(x=WIDTH // 2, y=HEIGHT - 100, projectiles_group=proj_group, screen_width=WIDTH, screen_height=HEIGHT)
    win_lose_system.player = player

    last_spawn = 0
    last_spawn_wave = 0

    # Initialize ticks_last_frame for delta_time calculation
    ticks_last_frame = pygame.time.get_ticks()

    while running:
        # Fill the screen with black background
        screen.fill(black_bg)

        # Calculate delta_time
        ticks = pygame.time.get_ticks()
        delta_time = (ticks - ticks_last_frame) / 1000.0  # Convert to seconds
        ticks_last_frame = ticks

        # Update timer based on delta_time
        timer.update(delta_time)

        # Handle collisions between projectiles and targets
        check_projectile_enemy_collisions(proj_group, enemy_group, damage=1)  # Player bullets damaging enemies
        check_player_projectile_collisions(player, enemy_projectiles, damage=10)  # Enemy bullets damaging player

        # Update all projectiles
        proj_group.update(False)
        enemy_projectiles.update(False)

        # Draw player and projectiles
        player.handle_input()
        player.draw(screen)
        proj_group.draw(screen)  # Draw player projectiles
        enemy_projectiles.draw(screen)  # Draw enemy projectiles

        # Update obstacles with delta_time
        for obstacle in obstacle_group:
            obstacle.update(None, delta_time)
            obstacle.draw(screen)

        # Spawn enemies at regular intervals
        if not timer.stopped and len(enemy_group) < max_enemies and timer.elapsed_time - last_spawn >= 3:
            spawnEnemy(enemy_group, timer.elapsed_time)
            last_spawn = timer.elapsed_time

        # Spawn a wave of enemies every minute, ignoring the max restriction
        if not timer.stopped and timer.elapsed_time - last_spawn_wave >= 60:
            for _ in range(3):  # Spawn 3 enemies as a wave
                spawnEnemy(enemy_group, timer.elapsed_time)
            last_spawn_wave = timer.elapsed_time

        # Update each enemy, allow them to fire shots
        for enemy in enemy_group:
            enemy.update(paused=False)
            enemy.fire_shot(enemy_projectiles, paused=False, curr=timer.elapsed_time)

            # Check for collision between player and enemy
            if player.is_alive and player.rect.colliderect(enemy.rect):
                player.take_dmg(10)
                if not player.is_alive:
                    print("Player defeated!")

            # Check if enemy is destroyed
            if not enemy.living:  # Assuming `enemy.living` becomes False when health is depleted
                # Play explosion sound
                ship_destroyed_sound.play()

                # Create explosion effect at the enemy's position
                dest_enemies.append((enemy.rect.center, pygame.time.get_ticks(), 20))  # explosion size 20

                ##increase score for kill
                score_system.increase(10) ##increase by 10 points

                # Remove enemy from group
                enemy.kill()

        # Draw enemies
        enemy_group.draw(screen)

        # Update and display the timer and score
        draw_text(f"{timer.elapsed_time:.2f}", small_font, NEON_CYAN, screen, 100, 100)
        score_display.display_score(score_system.get_score())

        # Update the game state (e.g., win/lose conditions)
        current_game_state = win_lose_system.update()

        # Handle events for quitting, shooting, saving, and loading
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    timer.stop()
                elif event.key == pygame.K_SPACE:
                    player.shoot()  # Player shoots, adding bullets to proj_group
                elif event.key == pygame.K_s:
                    message, start_time = user_save_and_load.saveHandling(score_system.get_score(), timer.elapsed_time)
                    save_text_show = True
                elif event.key == pygame.K_l:
                    message, start_time, score_system.score, timer.elapsed_time = user_save_and_load.loadHandling(score_system.get_score(), timer.elapsed_time)
                    save_text_show = True

        # Display save/load message if applicable
        if save_text_show:
            current_time = pygame.time.get_ticks()
            if current_time - start_time < 1500:
                draw_text(message, smaller_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 250)
            else:
                save_text_show = False

        # Handle explosion effects
        for enemy_center, time_destroyed, size in dest_enemies[:]:
            if pygame.time.get_ticks() - time_destroyed <= 250:
                pygame.draw.circle(screen, (200, 180, 0), enemy_center, size)
            else:
                dest_enemies.remove((enemy_center, time_destroyed, size))

        # Despawn enemies if needed
        despawnEnemy(to_despawn)

        # Update the display and frame rate
        pygame.display.flip()
        clock.tick(FPS)







