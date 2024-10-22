from tools.game_states import GameState

class WinLoseSystem:
    def __init__(self, score_system):
       ## self.player = player
        self.score_system = score_system
        self.state = GameState.ONGOING
        ##self.win_score = win_score ## Score required to win, sent from level in future (?)

    def check_win_condition(self): # Check if the player has won, TODO: Change logic later maybe
        if self.score_system.score >= 1000:  # Example score-based win condition
            self.state = GameState.WIN
            self.trigger_win()
        ###elif self.enemies_killed.score >= 50:  # TODO: PLACEHOLDER, can add different win logic
        ###    self.state = GameState.WIN
        ###    self.trigger_win()

    def check_lose_condition(self): # Check if the player has lost
        pass
        ##if self.player.health <= 0:  # Player health-based lose condition
        ##    self.state = GameState.LOSE
        ##    self.trigger_lose()

    def trigger_win(self):
        print("win state triggered!")

    def trigger_lose(self):
        print("lose state triggered!")

    def update(self):
        self.check_win_condition()
        self.check_lose_condition()

    def get_game_state(self):
        return self.state