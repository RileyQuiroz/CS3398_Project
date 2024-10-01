import json
import os

class Leaderboard:
    def __init__(self, filename):
        self.high_scores = []
    
        file_path = os.path.join('savedata', 'leaderboard.json')
        with open(file_path, 'r') as leaderboard_file:
            self.high_scores = json.load(leaderboard_file)

    def compare_score(self, score):
        for i in range(0, 10):
            if (not self.high_scores[i]) or self.high_scores[i] < score:
                self.update_list(score)

    def update_list(self, score):
        # Update leaderboard to insert new high score at position i,
        # pushing every lower score down the list
        self.high_scores[i:] = score, *self.high_scores[i:-1]
