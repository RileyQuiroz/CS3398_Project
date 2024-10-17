import pygame
import sys
from tools.timer import Timer
from tools.score_counter import Score
from tools.score_display import ScoreDisplay
from savesystem.leaderboard import Leaderboard
from savesystem import user_save_and_load
from obstacles.Obstacle import Obstacle
from characters.enemies.enemy_type_a import EnemyTypeA

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

# Define an in-game obstacle
obstacle = Obstacle(50, (200, 200), WHITE)

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

# Define framerate, clock, and in-game timer
FPS = 60
clock = pygame.time.Clock()
timer = Timer()
timer.start()

# Initialize Score and ScoreDisplay
score_system = Score()
score_display = ScoreDisplay(screen, font_size=36, color=NEON_CYAN, position=(50, 50))

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

def game_loop():
    # Create enemy for testing
    enemy_group = pygame.sprite.Group()
    #test_enemy = Enemy(health=10, pattern=0, x=100, y=100)
    enemy_group.add(EnemyTypeA(100, 100))
    
    save_text_show = False
    running = True

    # Fill screen with black background
    black_bg = (0, 0, 0)

     # Initialize variable for score testing/logic
    last_score_increase_time = 0  # Time of last score increase
    combo_time_limit = 300.0  # Time window for maintaining score combo

    # Initialize ticks
    ticks = 0.0
    ticks_last_frame = 0.0

    # Reset and start the timer
    timer.reset()
    timer.start()

    while running:
        screen.fill(black_bg)

        # Update timer and score during the game
        ticks = clock.get_time()
        delta_time = (ticks - ticks_last_frame) / 1000.0
        ticks_since_last_frame = ticks
        timer.update(delta_time)

        # Get current time (for scoring purposes)
        current_time = round(timer.elapsed_time, 2)

        # Display timer and score
        small_font = pygame.font.Font("assets/fonts/Future Edge.ttf", 32)
        draw_text(str(current_time), small_font, NEON_CYAN, screen, 100, 100)
        score_display.display_score(score_system.get_score())
        obstacle.draw(screen)
        
        # Update enemy position
        for enemy in enemy_group:
            enemy.update(WIDTH)
        # Draw all enemies that exist
        enemy_group.draw(screen)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to return to menu
                    running = False
                    timer.stop()
                if event.key == pygame.K_s: # Press S to save game
                    message, start_time = user_save_and_load.saveHandling(score_system.get_score(), timer.elapsed_time)
                    save_text_show = True
                if event.key == pygame.K_l: # Press L to load game
                    message, start_time, score_system.score, timer.elapsed_time = user_save_and_load.loadHandling(score_system.get_score(), timer.elapsed_time)
                    save_text_show = True
                if event.key == pygame.K_SPACE:  # Press SPACE to increase score (Testing)
                    timer.toggle()

                    time_since_last_increase = current_time - last_score_increase_time
                    # If within combo time limit (3 seconds), increase combo count (AKA faster pressing space = more points)
                    if time_since_last_increase <= combo_time_limit:
                        score_system.increase_combo(1)
                    else:
                        score_system.reset_combo()  # Reset combo if too late
                    
                    score_system.increase(10)  # Increase score by base points, multiplied by the current multiplier
                    last_score_increase_time = current_time

        # Keeps message on screen for 1.5 seconds
        current_time = pygame.time.get_ticks()
        if save_text_show and current_time - start_time < 1500:
            draw_text(message, smaller_font, WHITE, screen, WIDTH // 2 - 0, HEIGHT // 2 + 250)
        else:
           save_text_show = False
        pygame.display.flip()
        clock.tick(60)

