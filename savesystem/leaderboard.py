import json
import os

class Leaderboard:
    def __init__(self, filename):
        self.high_scores = []
        self.file_path = os.path.join('savedata', filename)
        with open(self.file_path, 'r') as leaderboard_file:
            self.high_scores = json.load(leaderboard_file)

    def compare_score(self, score):
        for i in range(0, 10):
            if (not self.high_scores[i]) or self.high_scores[i] < score:
                self.update_list(score)

    def update_list(self, score):
        # Update leaderboard to insert new high score at position i,
        # pushing every lower score down the list
        self.high_scores[i:] = score, *self.high_scores[i:-1]

    def save(self):
        with open(self.file_path, 'w') as save_file:
            json.dump(self.high_scores, save_file)