import pygame
import random

planet_images = [
    pygame.image.load('assets/Planets/Ice.png'),
    pygame.image.load('assets/Planets/Lava.png'),
    pygame.image.load('assets/Planets/Terran.png'),
    pygame.image.load('assets/Planets/Baren.png'),
    pygame.image.load('assets/Planets/Black_hole.png')
]

class Background:
    def __init__(self, screen):
        self.screen = screen
        self.stars = [[random.randint(0, 800), random.randint(0, 600), random.uniform(0.5, 2)] for _ in range(100)]
        self.planets = []
        for _ in range(3):
            x = random.randint(0, 800)
            y = random.randint(-300, 600)
            size = random.randint(80, 150)
            speed = random.uniform(0.05, 0.3)
            image = random.choice(planet_images)
            self.planets.append([x, y, size, speed, pygame.transform.scale(image, (size, size))])

    def update(self):
        for star in self.stars:
            star[1] += star[2]
            if star[1] > 600:
                star[0] = random.randint(0, 800)
                star[1] = random.randint(-50, -10)
                star[2] = random.uniform(0.5, 2)

        for planet in self.planets:
            planet[1] += planet[3]
            if planet[1] > 600:
                planet[0] = random.randint(0, 800)
                planet[1] = random.randint(-300, -100)
                planet[2] = random.randint(80, 150)
                planet[3] = random.uniform(0.05, 0.3)
                planet_image = random.choice(planet_images)
                planet[4] = pygame.transform.scale(planet_image, (planet[2], planet[2]))

    def draw(self):
        self.screen.fill((0, 0, 0))
        for star in self.stars:
            pygame.draw.circle(self.screen, (255, 255, 255), (int(star[0]), int(star[1])), 2)
        for planet in self.planets:
            self.screen.blit(planet[4], (int(planet[0]), int(planet[1])))
