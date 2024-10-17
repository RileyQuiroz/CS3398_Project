import pygame
class Enemy(pygame.sprite.Sprite):
    def __init__(self, health = 1, pattern = 0, x = 0, y = 0):
        super().__init__()
        self.health = health
        self.living = True
        self.color = (255, 0, 0) # Default red color, will change when we have sprites
        self.pos_x = x
        self.pos_y = y
        self.size = 10
        self.velocity = 2
        # Next 3 lines are for ship's image on screen
        self.image = pygame.Surface((self.size, self.size)) 
        self.image.fill(self.color)  
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
            
    def decrease_health(self, damage = 1): # returns true if enemy still alive, false otherwise
        self.health -= damage
        if(self.health < 1):
            self.living = False
            self.kill()
        
    def fire_shot(self):
        print("Can't shoot yet")
        # if bullet pattern 0, ship type a pattern
        # else if bullet pattern 1, ship type b pattern
    
    def update(self, screen_width): # Updates position
        pass
        
    def draw(self, surface): # Displays enemy to screen
        pass

    