class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.difficulty = 1.0  # TODO: Maybe handle this differently later

    def start_next_level(self):
        self.current_level += 1
        print(f"Starting Level {self.current_level} with difficulty {self.difficulty}")

    def get_current_level(self):
        return self.current_level
