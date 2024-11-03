from obstacles.Obstacle import Obstacle

class Dangerous(Obstacle):
    def __init__(self, position, sprite_path):
        super().__init__(position, sprite_path)
    
    def handle_player_collision(self, player):
        super().handle_player_collision(player)

        player.health -= 1