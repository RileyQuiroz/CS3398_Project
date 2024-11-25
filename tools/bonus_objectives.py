import random
import pygame
import time

class BonusObjective:
    def __init__(self, description):
        """
        Initialize a BonusObjective.
        :param description: The description of the objective.
        """
        self.description = description
        self.completed = False

    def initialize(self, player, level):
        """
        Set up any necessary tracking variables.
        :param player: The player object.
        :param level: The level object.
        """
        pass  # To be overridden in subclasses

    def check_completion(self, player, level, elapsed_time):
        """
        Check if the objective is completed.
        :param player: The player object.
        :param level: The level object.
        """
        pass  # To be overridden in subclasses


class NoDamageObjective(BonusObjective):
    def __init__(self):
        super().__init__("Take no damage in the first two levels")

    def initialize(self, player, level):
        self.starting_health = player.health

    def check_completion(self, player, level, elapsed_time):
        self.completed = player.health == self.starting_health
        return self.completed

class UnderTimeObjective(BonusObjective):
    def __init__(self):
        super().__init__("Complete the first two levels in under 45 seconds")

    def initialize(self, player, level):
        pass

    def check_completion(self, player, level, elapsed_time):
        #elapsed_time = level.elapsed_time - level.start_time ## FIXME!!
        self.completed = elapsed_time - level.level_start_time <= 45
        return self.completed

# TODO: Player does NOT have shots_fired and shots_hit variable, will have to figure out a way to do this later
class AccuracyObjective(BonusObjective):
    def __init__(self):
        super().__init__("Achieve 80%+ accuracy in the first two levels")

    def initialize(self, player, level):
        # No direct changes to the player object needed
        pass

    def check_completion(self, player, level, elapsed_time):
        accuracy = level.get_accuracy()
        self.completed = accuracy >= 0.8
        print("shots fired: ", level.player_tracker.shots_fired)
        print("shots hit: ", level.player_tracker.shots_hit)
        return self.completed



class KillStreakObjective(BonusObjective):
    def __init__(self):
        super().__init__("Achieve a kill streak of 5")

    def initialize(self, player, level):
        player.kill_count = 0

    def check_completion(self, player, level, elapsed_time):
        self.completed = player.kill_count >= 10
        print("check completion killstreakobjective reached!")
        return self.completed


class BonusObjectiveDisplay:
    def __init__(self, objectives, font, screen, position=(10, 10), spacing=30):
        """
        Initialize the display for bonus objectives.
        
        :param objectives: List of BonusObjective objects.
        :param font: Pygame font object for rendering text.
        :param screen: Pygame screen where the objectives will be rendered.
        :param position: Top-left position for the first objective.
        :param spacing: Vertical spacing between objectives.
        """
        self.objectives = objectives
        self.font = pygame.font.Font("assets/fonts/Future Edge.ttf", 16)
        self.screen = screen
        self.position = position
        self.spacing = spacing

    def draw(self):
        """
        Draw the objectives on the screen.
        """
        x, y = self.position
        for objective in self.objectives:
            color = (0, 255, 0) if objective.completed else (155, 0, 255)  # Green if completed, white otherwise, Maybe change colors
            text_surface = self.font.render(objective.description, True, color)
            self.screen.blit(text_surface, (x, y))
            y += self.spacing