import pygame
class Enemy:
    def __init__(self, type = 0, health = 1, pattern = 0, position = (10, 10)):
        self.type = type # Will not have type 0 for final product
        self.health = health
        self.living = True
        self.bullet_pattern = pattern # Determines projectile pattern
        self.position = position
            
    def decrease_health(self, damage = 1): # returns true if enemy still alive, false otherwise
        self.health -= damage
        if(self.health < 1):
            self.living = False
        return self.living
        
    def fire_shot(self):
        print("Can't shoot yet")
        # if bullet pattern 0, ship type a pattern
        # else if bullet pattern 1, ship type b pattern
    
    def move_enemy(self):
        #if enemy type 1, use ship type a move pattern
        # for now, just moves from right to left
        mover = 1
        if self.position >= 800:
            mover = -1
        else:
            mover = 1
        self.position += mover
        print("on the move")
        
    def display_enemy(self, surface):
        #if self.type = 0
        pygame.draw.circle(surface) #color position, radius)

    