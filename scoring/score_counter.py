## This class represents the score of the player
class Score:
    def __init__(self) -> None:
        self.score = 0
        self.multiplier = 1
        self.combo_count = 0

    # Increase score by points and current multiplier
    def increase(self, points) -> None:
        self.score += points * self.multiplier
    
    # Increase score with flat points
    def increase_flat(self, points) -> None:
        self.score += points

    # Reset score and combo count
    def reset(self) -> None:
        self.score = 0
        self.combo_count = 0
        self.multiplier = 1
    
    # Set multiplier, capped at 5
    def set_multiplier(self, multiplier) -> None:
        self.multiplier = min(multiplier, 5)
    
    # Increase combo count and update multiplier
    def increase_combo(self, combo) -> None:
        self.combo_count += combo
        self.update_multiplier()

    # Reset combo
    def reset_combo(self) -> None:
        self.combo_count = 0
        self.multiplier = 1

    ## Multiplier will increase depending on combo count, capped at 5
    def update_multiplier(self) -> None:
        if self.combo_count % 5 == 0:
            self.multiplier = min(self.multiplier + 1, 5)

    def get_score(self) -> int:
        return self.score