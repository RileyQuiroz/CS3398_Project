import pygame
import sys
from timer import Timer

# Initialize pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("BULLETHELL - Timer Test")

def test_loop():
    clock = pygame.time.Clock()
    test_timer = Timer()

    # Start the timer
    test_timer.start()

    # Run the test game loop
    while True:
        # Get time elasped since last frame
        dt = clock.tick(60) / 1000
        
        # Update the timer
        test_timer.update(dt)

        # Handle events
        for event in pygame.event.get():
            # If any key is pressed, stop the timer and
            # end the test loop
            if event.type == pygame.KEYDOWN:
                test_timer.stop()
            if event.type == pygame.QUIT:
                # Print the elapsed time and end the test
                print("Elapsed Time:", test_timer.elapsed_time, "seconds") 
                pygame.quit()
                sys.exit()

        # Update the display
        pygame.display.update()            
