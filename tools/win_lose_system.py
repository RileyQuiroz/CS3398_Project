import pygame
from tools.game_states import GameState

class WinLoseSystem:
    def __init__(self, score_system, player=None):
        self.score_system = score_system
        self.state = GameState.ONGOING
        self.player = player  # Player object for health checks, life checks, etc.

    def check_win_condition(self):
        """Check if the player has won based on the score, could add more parameters."""
        if self.score_system.score >= 50:  # Example score-based win condition
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
        pygame.mixer.Sound("assets\sound_efx\game_win.ogg").play()

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