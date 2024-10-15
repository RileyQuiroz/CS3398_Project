class Enemy:
    def __init__(self):
        self.health = 1
        self.living = True
        self.enemy_type = 0 # Will be used to determine the type of enemy
        self.bullet_pattern = 0 # Determines bullet pattern for firing pellets
        
    def check_if_alive(self):
        if(self.health < 1):
            self.living = False
            # Then remove the destroyed enemy
            
    def decrease_health(self):
        self.health = self.health - 1