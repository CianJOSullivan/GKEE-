import pygame
import json

class Timer:
    def __init__(self) -> None:
        self.data = "data.json"
        self.timer = 0
        self.running = False
        self.splits = []
        self.attempts = 0
        self.world_record = []
        self.personal_best = []
        self.finished = False


    def start(self):
        self.running = True 
        self.attempts += 1
        self.load_data()


    def get_time(self): 
        seconds = self.timer // 60
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes:02}:{remaining_seconds:02}"
    

    def split(self):
        self.splits.append(self.timer)


    def get_splits(self):
        return [self.get_time(t) for t in self.splits]
    

    def load_data(self):
        with open(self.data, "r") as file:
            data = json.load(file)
        self.world_record = data["timing"]["world_record"]["splits"]
        self.personal_best = data["timing"]["personal_best"]["splits"]
        self.attempts = data["attempts"]
        self.world_record = [int(i) for i in self.world_record]
        self.personal_best = [int(i) for i in self.personal_best]
        self.attempts = int(self.attempts)

       
    def save_data(self):
        if self.finished:
            with open(self.data, "w") as file:
                if len(self.splits) == len(self.world_record):
                    if self.splits[-1] < self.personal_best[-1]:
                        self.personal_best = self.splits
                    if self.splits[-1] < self.world_record[-1]:
                        self.world_record = self.splits
                data = {
                    "timing": {
                        "world_record": {
                            "splits": self.world_record
                        },
                        "personal_best": {
                            "splits": self.personal_best
                        }
                    },
                    "attempts": self.attempts
                }
                json.dump(data, file, indent=4)


    def reset(self):
        self.timer = 0
        self.splits = []
        self.running = False
        self.finished = False
        self.load_data()


    def check_finished(self):
        if len(self.splits) == len(self.world_record):
            self.finished = True
            self.running = False
            
        
    def get_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.running and not self.finished:
                    self.split()
                    self.check_finished()
                elif not self.running and not self.finished:
                    self.start()
            elif event.key == pygame.K_RETURN:
                self.save_data()
                self.reset()
    

    def run(self):
        if self.running:
            self.timer += 1