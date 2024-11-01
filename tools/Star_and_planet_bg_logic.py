import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))

# Set up clock to control frame rate
clock = pygame.time.Clock()

# Load multiple planet images into a list
planet_images = [
    pygame.image.load('assets/Planets/Ice.png'),
    pygame.image.load('assets/Planets/Lava.png'),
    pygame.image.load('assets/Planets/Terran.png'),
    pygame.image.load('assets/Planets/Baren.png'),
    pygame.image.load('assets/Planets/Black_hole.png')
]

# Function to scale the planet image
def scale_planet(image, size):
    return pygame.transform.scale(image, (size, size))

# Create a list to store stars (x, y, speed)
stars = []
for _ in range(100):
    x = random.randint(0, 800)
    y = random.randint(0, 600)
    speed = random.uniform(0.5, 2)  # Slower speed range for stars
    stars.append([x, y, speed])

# Create a list to store planets (x, y, size, speed, image)
planets = []
for _ in range(3):  # Reduce number of planets to make them appear less frequently
    x = random.randint(0, 800)
    y = random.randint(-300, 600)  # Planets can start higher to make them appear less frequently
    size = random.randint(80, 150)  # Increase the size range for larger planets
    speed = random.uniform(0.05, 0.3)  # Slower movement for larger planets
    planet_image = random.choice(planet_images)  # Randomly choose a planet image
    scaled_image = scale_planet(planet_image, size)  # Scale the planet image based on size
    planets.append([x, y, size, speed, scaled_image])  # Store planet data with image

def draw_stars():
    screen.fill((0, 0, 0))  # Black background

    # Update and draw each star
    for star in stars:
        star[1] += star[2]  # Move the star downward by its speed
        if star[1] > 600:  # Reset star at the top
            star[0] = random.randint(0, 800)
            star[1] = random.randint(-50, -10)
            star[2] = random.uniform(0.5, 2)

        # Draw the star
        pygame.draw.circle(screen, (255, 255, 255), (int(star[0]), int(star[1])), 2)

def draw_planets():
    # Update and draw each planet
    for planet in planets:
        planet[1] += planet[3]  # Move the planet downward by its speed
        if planet[1] > 600:  # Reset planet at the top when it moves off-screen
            planet[0] = random.randint(0, 800)
            planet[1] = random.randint(-300, -100)  # Reset planet higher up for less frequent appearance
            planet[2] = random.randint(80, 150)  # Randomize size again for larger planets
            planet[3] = random.uniform(0.05, 0.3)  # Randomize speed again for slower planets
            planet_image = random.choice(planet_images)  # Randomly choose a new planet image
            planet[4] = scale_planet(planet_image, planet[2])  # Rescale the planet image for its new size

        # Draw the planet image
        screen.blit(planet[4], (int(planet[0]), int(planet[1])))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the moving stars
    draw_stars()

    # Draw the moving planets
    draw_planets()

    # Update the display
    pygame.display.update()

    # Cap the frame rate at 60 FPS
    clock.tick(60)

pygame.quit()
