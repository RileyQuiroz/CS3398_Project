from obstacles.Destructible import Destructible
from tools.score_counter import Score
from tools.sounds import Sounds

class Friend(Destructible):
    def __init__(self, position, health, score_system, scale, sprite_path):
        super().__init__(position, health, score_system, scale, sprite_path)

        self.color = (75, 175, 75)

    def take_damage(self):
        self.health -= 1

        if self.health <= 0:
            self.destroyed = True
            self.score_system.decrease_flat(50)
            Sounds.ship_destroyed.play()
