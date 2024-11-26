from tools.timer import Timer

class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.difficulty = 1.0  # TODO: Maybe handle this differently later
        self.level_start_time = 0.0

    def start_next_level(self):
        self.current_level += 1
        self.level_start_time = self.get_level_start_time()
        print(f"Starting Level {self.current_level} with difficulty {self.difficulty} with start time of {self.level_start_time}")

    def get_current_level(self):
        return self.current_level
    
    def get_level_start_time(self):
        self.level_start_time = Timer.elapsed_time