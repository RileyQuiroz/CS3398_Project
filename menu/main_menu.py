import pygame
import sys
from timer import Timer
from score_counter import Score
from score_display import ScoreDisplay

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

# Define in-game timer
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

        # Update in-game timer
        if not timer.stopped:
            timer.update(1.0)

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
            back_color = NEON_PURPLE if hovered['back'] else WHITE

            ##################THESE WILL BE MOVED INTO GAME LOOP, TIME AND DISPLAY SCORE ARE HERE FOR TESTING PURPOSES###################### 

            # Draw the timer on the screen
            small_font = pygame.font.Font("assets/fonts/Future Edge.ttf", 32)  # Set the size to 32 for the timer
            timer_rect = draw_text(str(timer.elapsed_time), small_font, NEON_CYAN, screen, 100, 100)

            # Display the score
            score_display.display_score(score_system.get_score())

            ##############################################################################################################################

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
            draw_text('Records', font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 150)
            back_color = NEON_PURPLE if hovered['back'] else WHITE
            back_rect = draw_text('Back', font, back_color, screen, WIDTH // 2, HEIGHT // 2 + 150)

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
            draw_text_left_aligned('Difficulty', small_font, WHITE, screen, 50, HEIGHT // 2 - 50)
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
                        # Add start game logic here
                    elif records_rect.collidepoint(event.pos):
                        current_menu = 'records'  # Switch to Records menu
                    elif settings_rect.collidepoint(event.pos):
                        current_menu = 'settings'  # Switch to Settings menu
                    elif quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

                    ######################THIS EVENT IS TO TEST THE TIMER WILL NEED TO BE REMOVED###############################
                    # Handle timer pause/resume toggle
                    if timer_rect.collidepoint(event.pos):
                    #####################################################################################################
                        timer.stopped = not timer.stopped
                        

                elif current_menu in ['records', 'settings']:
                    # Handle "Back" button in Records or Settings
                    if back_rect.collidepoint(event.pos):
                        current_menu = 'main'  # Switch back to Main menu

        # Update the display
        pygame.display.update()
