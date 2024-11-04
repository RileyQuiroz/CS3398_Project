from obstacles.Destructible import Destructible
from tools.score_counter import Score

class Friend(Destructible):
    def __init__(self, position, health, score_system, sprite_path):
        super().__init__(position, health, sprite_path)

        self.score_system = score_system
        self.color = (75, 175, 75)

    def take_damage(self):
        self.health -= 1

        if self.health <= 0:
            self.destroyed = True
            self.score_system.decrease_flat(50)
