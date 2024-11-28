import json
import os

class Leaderboard:
    def __init__(self, filename):
        self.file_path = os.path.join('savesystem/savedata/', filename)
        self.high_scores = self.load_leaderboard()

    def load_leaderboard(self):
        try:
            with open(self.file_path, 'r') as leaderboard_file:
                return json.load(leaderboard_file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Default leaderboard if file doesn't exist
            return [["JS", 1500], ["OM", 1000], ["EA", 500], ["RQ", 250]]

    def compare_score(self, score):
        for i, entry in enumerate(self.high_scores):
            if score > entry[1]:
                return i  # Return the position to insert the new score
        return None

    def update_list(self, position, initials, score):
        # Insert the new high score
        self.high_scores.insert(position, [initials, score])

        # Keep ONLY the top 4 entries
        self.high_scores = self.high_scores[:4]

    def save(self):
        with open(self.file_path, 'w') as save_file:
            json.dump(self.high_scores, save_file)
