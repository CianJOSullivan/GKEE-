import pygame
import json
import time

class Timer:
    def __init__(self) -> None:
        self.data = "../data/data.json"
        self.timer = 0
        self.running = False
        self.splits = []
        self.attempts = 0
        self.world_record = []
        self.personal_best = []
        self.wr_difference = []
        self.pr_difference = []
        self.finished = False
        self.start_time = 0
        self.split_number = 0
        self.load_data()


    def get_splits(self):
        return self.splits
    
    def set_splits(self, splits):
        self.splits = splits
    

    def start(self):
        self.running = True 
        self.start_time = time.time()
        self.load_data()
        self.split_number = 0 


    def get_time(self): 
        if self.running and not self.finished:
            seconds = int(round(time.time() - self.start_time, 0))
        elif self.finished:
            seconds = self.splits[-1]
        else:
            seconds = 0
   
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes:02}:{remaining_seconds:02}"
    

    def split(self):
        self.splits.append(int(round(time.time() - self.start_time, 0)))
        self.split_number += 1
        pr = self.splits[-1] - self.personal_best[self.split_number - 1]
        wr = self.splits[-1] - self.world_record[self.split_number - 1]
        self.wr_difference.append(wr)
        self.pr_difference.append(pr)
        

    def return_visual_splits(self):
        return self.wr_difference, self.pr_difference


    def load_data(self):
        with open(self.data, "r") as file:
            data = json.load(file)
        self.world_record = data["timing"]["world_record"]["splits"]
        self.personal_best = data["timing"]["personal_best"]["splits"]
        self.attempts = data["attempts"]
        self.world_record = [int(i) for i in self.world_record]
        self.personal_best = [int(i) for i in self.personal_best]
        self.attempts = int(self.attempts)


    def get_personal_record(self):
         return self.pr_difference
    

    def get_world_record(self):
        return self.wr_difference

    def save_data(self):
        with open(self.data, "w") as file:
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

    def update_records(self):
        if len(self.splits) == len(self.world_record):
            if self.splits[-1] < self.personal_best[-1]:
                self.personal_best = self.splits
            if self.splits[-1] < self.world_record[-1]:
                self.world_record = self.splits
        self.save_data()


    def reset(self):
        self.timer = 0
        self.splits = []
        self.running = False
        self.finished = False
        self.start_time = 0
        self.wr_difference = []
        self.pr_difference = []
        self.attempts += 1  
        self.save_data() 
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
                    self.return_visual_splits()
                elif not self.running and not self.finished:
                    self.start()
            elif event.key == pygame.K_RETURN:
                self.reset() 
    def get_attempts(self):
        return self.attempts
