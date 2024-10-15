# The Obstacle class represents an in-game object that can
# impede the player in some way.
class Obstacle:
    def __init__(self, radius, position, sprite):
        self.radius = radius
        self.position = (0, 0)
        self.velocity = (0, 0)
        self.sprite = 0
        self.is_colliding = False

    def load_sprite(self, sprite):
        pass

    def check_for_player_collision(self, player):
        # Calculate the slope between the player's position and the
        # obstacle's position. If the slope is less than the sum of
        # the radii of the two objects, they are colliding.
        slope = (player.position.y - self.position.y) / (player.position.x - self.position.x)
        self.is_colliding = abs(slope) < self.player.radius

    def update(self, player, dt):
        self.check_for_player_collision(player)

        if not self.is_colliding:
            self.position.x = self.position.x + (self.velocity.x * dt)
            self.position.y = self.position.y + (self.velocity.y * dt)

