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
background = pygame.image.load("assets/backgrounds/space_background.png")  # Load your space background image
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Define colors
NEON_CYAN = (0, 255, 255)
NEON_PURPLE = (155, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load a futuristic font (if you have one)
font = pygame.font.Font("assets/fonts/Future Edge.ttf", 74)

# Load hover sound
hover_sound = pygame.mixer.Sound("assets/sound_efx/hover_sound.wav")  # Replace with your sound file

# Define in-game timer
timer = Timer()
timer.stopped = False

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
        'quit': False
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

            # Draw the timer on the screen
            #timer_rect = draw_text(str(timer.elapsed_time), font, NEON_CYAN, screen, 100, 100)
            # Load a smaller font for the timer
            small_font = pygame.font.Font("assets/fonts/Future Edge.ttf", 32)  # Set the size to 32 for the timer

            # Draw the timer with the smaller font
            timer_rect = draw_text(str(timer.elapsed_time), small_font, NEON_CYAN, screen, 100, 100)

             # Display the score (this will update every frame)
            score_display.display_score(score_system.get_score())

            # Check if mouse is hovering over the options
            # If it is hovering and was not before, play the hover sound and change the hover state
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
                        score_system.increase(10)  # Increase score by 10 points for testing, ** THIS IS FOR TESTING PURPOSES **
                        # Add start game logic here
                    elif records_rect.collidepoint(event.pos):
                        current_menu = 'records'  # Go to the Records menu
                    elif settings_rect.collidepoint(event.pos):
                        current_menu = 'settings'  # Go to the Settings menu
                    elif quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

                    # Handle timer pause/resume toggle
                    if timer_rect.collidepoint(event.pos):
                        timer.stopped = not timer.stopped

        # Update the display
        pygame.display.update()