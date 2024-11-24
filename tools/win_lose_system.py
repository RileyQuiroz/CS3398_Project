import pygame
import time
from tools.game_states import GameState

class WinLoseSystem:
    def __init__(self, score_system, player=None):
        self.score_system = score_system
        self.player = player  # Player object for health, life checks, etc.
        self.state = GameState.ONGOING
        self.current_level = 1
        self.difficulty = 1.0  # Adjustable per level
        self.level_start_time = 0.0
        self.level_processed = set()  # Flags for levels where win conditions were processed

    # --- Level Management ---
    def start_next_level(self, elapsed_time, current_objectives):
        """Advance to the next level and reset necessary parameters."""
        self.current_level += 1
        self.level_start_time = elapsed_time  # Record the time the level starts
        self.difficulty = 1  # TODO: Maybe handle difficulty differently

        for obj in current_objectives:
            if obj.check_completion(self.player, self.current_level-1):
                print(f"Objective '{obj.description}' passed!")
            else:
                print(f"Objective '{obj.description}' failed.")

        print("start next level reached!")
        print(f"Starting Level {self.current_level} with difficulty {self.difficulty} with time of {elapsed_time}")
        return self.current_level

    def get_elapsed_time(self):
        """Calculate and return elapsed time for the current level."""
        return time.time() - self.level_start_time

    def reset_level_timer(self, elapsed_time):
        """Manually reset the timer, if needed."""
        self.level_start_time = elapsed_time

    # --- Win and Lose Conditions ---
    def check_win_condition(self, elapsed_time, current_objectives):
        """Determine if the player has met the win condition for the current level."""
        if self.current_level == 1 and self.score_system.score >= 50 and 1 not in self.level_processed:
            print("Level 1 win condition met! Proceeding to level 2.")
            self.level_processed.add(1)
            self.start_next_level(elapsed_time, current_objectives)
        elif self.current_level == 2 and self.score_system.score >= 100 and 2 not in self.level_processed:
            print("Level 2 win condition met! Proceeding to level 3.")
            self.level_processed.add(2)
            self.start_next_level(elapsed_time, current_objectives)
        elif self.current_level == 3 and self.score_system.score >= 150 and 3 not in self.level_processed:
            print("Final level win condition met! You win!")
            self.trigger_win()
            self.state = GameState.WIN  # Update state to WIN
        return self.state

    def check_lose_condition(self):
        """Check if the player has lost."""
        if self.player.health <= 0:
            print("Player health is 0. Game over!")
            self.trigger_lose()
            self.state = GameState.LOSE
        return self.state

    def trigger_win(self):
        """Handle win scenario."""
        print("Win state triggered!")
        pygame.mixer.Sound("assets/sound_efx/game_win.ogg").play()

    def trigger_lose(self):
        """Handle lose scenario."""
        print("Lose state triggered!")
        pygame.mixer.Sound("assets/sound_efx/game_over.mp3").play()

    # --- Game State Management ---
    def update(self, elapsed_time, current_objectives):
        """Update game state based on win and lose conditions."""
        self.check_win_condition(elapsed_time, current_objectives)
        self.check_lose_condition()
        return self.state

    def get_game_state(self):
        """Return the current game state."""
        return self.state

    def reset(self):
        """Reset the game to an initial state."""
        self.state = GameState.ONGOING
        self.current_level = 0
        self.level_processed.clear()
        self.player.health = 100
        self.player.is_alive = True
        self.score_system.reset()
