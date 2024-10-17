import pygame
class Enemy(pygame.sprite.Sprite):
    def __init__(self, health = 1, x = 0, y = 0):
        super().__init__()
        self.health = health
        self.living = True
        self.time_destroyed = 0
        self.color = (255, 0, 0) # Default red color, will change when we have sprites
        self.pos_x = x
        self.pos_y = y
        self.size = 10
        self.velocity = 2
        # Next 3 lines are for ship's image on screen
        self.image = pygame.Surface((self.size, self.size)) 
        self.image.fill(self.color)  
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
            
    def decrease_health(self, damage = 1):
        self.health -= damage
        if(self.health < 1):
            self.living = False
    
    def destroy_enemy(self, screen):
        self.kill()
        self.image = pygame.draw.circle(screen, (200, 180, 0), self.rect.center, self.size)     
        
    def fire_shot(self):
        pass
    
    def update(self, screen_width): # Updates position
        pass
        
    def draw(self, surface): # Displays enemy to screen
        pass

    