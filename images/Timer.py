# Timer represents the in-game clock that runs anytime
# the game has been started and has not been paused.
class Timer:
    def __init__(self):
        self.elapsed_time = 0.0
        self.stopped = True

    def start(self):
        self.stopped = False

    def stop(self):
        self.stopped = True

    def reset(self):
        self.elapsed_time = 0.0
        self.stopped = True

    def update(self, delta_time):
        if not self.stopped:
            self.elapsed_time = self.elapsed_time + delta_time
