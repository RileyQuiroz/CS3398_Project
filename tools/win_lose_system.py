import pygame
from tools.game_states import GameState
from tools.level_manager import LevelManager

class WinLoseSystem:
    def __init__(self, score_system, player=None):
        self.score_system = score_system
        self.state = GameState.ONGOING
        self.player = player  # Player object for health checks, life checks, etc.
        self.level_manager = LevelManager() # TODO: Maybe handle LevelManager differently later, and instead of score, use enemies/waves
        self.level_processed = set() # Flags for if level checks have been reached

    def check_win_condition(self):
        """Check if the player has won based on the score, could add more parameters."""
        current_level = self.level_manager.get_current_level()
        if current_level == 1 and self.score_system.score >= 50 and 1 not in self.level_processed:
            print("debug: level 1 win condition! Proceeding to level 2!")
            self.level_manager.start_next_level()
        elif current_level == 2 and self.score_system.score >= 100 and 2 not in self.level_processed:
            print("debug: level 2 win condition! Proceeding to level 3!")
            self.level_manager.start_next_level()
        elif current_level == 3 and self.score_system.score >= 150 and 3 not in self.level_processed:
            print("debug: Final level win condition! You won!")
            self.trigger_win()
            self.state = GameState.WIN  # Update state to WIN
        return self.state

    def check_lose_condition(self):
        """TODO: Check if the player has lost based on different parameters."""
        if self.player.health <= 0:
            self.trigger_lose()
            self.state = GameState.LOSE
        return self.state

    def trigger_win(self):
        print("Win state triggered!")
        pygame.mixer.Sound("assets/sound_efx/game_win.ogg").play()

    def trigger_lose(self):
        print("Lose state triggered!")
        pygame.mixer.Sound("assets/sound_efx/game_over.mp3").play()

    def update(self):
        """Update the game state by checking win and lose conditions."""
        self.check_win_condition()
        self.check_lose_condition()  # Call lose check after win check
        return self.state

    def get_game_state(self):
        """Return the current game state."""
        return self.state

    def reset(self):
        self.state = GameState.ONGOING
        self.player.health = 100
        self.player.is_alive = True