from obstacles.Obstacle import Obstacle

# The Dangerous class represents an obstacle that deals
# damage to the player upon collision
class Dangerous(Obstacle):
    def __init__(self, position, scale, sprite_path):
        super().__init__(position, scale, sprite_path)

        self.color = (175, 75, 75)

    def handle_player_collision(self, player):
        super().handle_player_collision(player)
        player.take_dmg(1)

    def update(self, player, dt):
        super().update(player, dt)
        player.got_hit = self.is_colliding
