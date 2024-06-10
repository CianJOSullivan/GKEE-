import pygame
from images import Abh, Nukes, Extra_Credit, Idle_Eyes, Reign_Drops, Shopping_Free
from settings import *
import time
import json
from logic import ValveLogic
from timer import Timer


class GorodKrovi:
    def __init__(self, window):
        self.win = window
        self.selected_states = {"DEPT": [0, 0, 0, 0, 0], "DRAGON": [0, 0, 0, 0, 0], "ARM": [0, 0, 0, 0, 0],
                                "SUPPLY": [0, 0, 0, 0, 0], "INF": [0, 0, 0, 0, 0], "TANK": [0, 0, 0, 0, 0]}
        self.locations = ["DEPT", "DRAGON", "ARM", "SUPPLY", "INF", "TANK"]
        self.results = []
        self.personal_records = []
        self.world_record = []
        self.split_names = ["Flight 1", "Flight 2", "Start Trophy", "Start Boss", "Finish"]
        self.gobblegum_images = [Reign_Drops, Idle_Eyes, Extra_Credit, Nukes, Abh]
        self.gobblegum_images = [pygame.transform.scale(image, (140, 140)) for image in self.gobblegum_images]
        self.gobblegum_images_gray = []
        self.gobblegum_names = ["Reign_Drops", "Idle_Eyes", "Extra_Credit", "Nukes", "Abh"]
        self.gobblegums = {"Reign_Drops": True, "Idle_Eyes": True, "Extra_Credit": True, "Nukes": True, "Abh": True}
        self.trophies = ["Spawn", "Eyebeam", "Tank", "Toilet", "Dragon S", "Bunker"]
        self.trophies_selected = {trophy: False for trophy in self.trophies}
        self.RESET_BUTTON_RECT = pygame.Rect(1050, 420, 170, 40)
        self.pressed_locations = []
        self.timer = Timer()
        self.valve_logic = ValveLogic("../data/valve.json")
        self.intialise()

    def intialise(self):
        for image in self.gobblegum_images:
            image_gray = image.copy()
            image_gray.fill((45, 45, 45, 255),
                            special_flags=pygame.BLEND_RGBA_MULT)
            self.gobblegum_images_gray.append(image_gray)

    def draw_text(self, text, font, color, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        self.win.blit(textobj, textrect)

    def draw_valve_buttons(self):
        x, y = 35, 470
        width = 140
        height = 40
        spacing = 5
        for valve_name in self.locations:
            for row in range(5):
                pygame.draw.rect(self.win, GREEN if self.selected_states[valve_name][row] else BLACK, (
                    x, y + (row * (spacing + height)), width, height))
            x += 170

    def draw_results_box(self):
        pygame.draw.rect(self.win, BLACK, (1050, 470, 170, 220))
        x, y = 1050, 470
        for result in self.results:
            text = NAME_FONT.render(result, True, WHITE)
            text_width = text.get_width()
            self.draw_text(result, NAME_FONT, WHITE, x +
                           10 + (text_width // 2), y + 20)
            y += 35

    def draw_valve_headings(self):
        x, y = 105, 450
        headings = self.locations.copy()
        headings.append("RESULTS")
        for name in headings:
            self.draw_text(name, NAME_FONT, BLACK, x, y)
            x += 170

    def draw_valve_text(self):
        x, y = 35, 470
        width = 140
        height = 40
        spacing = 5
        text_options = ["Green", "Cylinder", "1", "2", "3"]
        for valve_name in self.locations:
            for row in range(5):
                self.draw_text(text_options[row], NAME_FONT, BLACK if self.selected_states[valve_name][row]
                else WHITE, x + (width // 2), y + (row * (spacing + height)) + (height // 2))
            x += 170

    def draw_gobblegums(self):
        x, y = 75, 700
        spacing = 100
        for val, image in enumerate(self.gobblegum_images):
            name = self.gobblegum_names[val]
            if not self.gobblegums[name]:
                self.win.blit(self.gobblegum_images_gray[val], (x, y))
            else:
                self.win.blit(image, (x, y))
            x += 140 + spacing

    def draw_trophies(self):
        if not all(self.trophies_selected.values()):
            x, y = 125, 350
            spacing = 50
            for trophy in self.trophies:
                color = GREEN if self.trophies_selected[trophy] else RED
                text_surface = NAME_FONT.render(trophy, True, WHITE)
                text_rect = text_surface.get_rect()
                text_rect.x -= text_rect.width // 2
                self.draw_text(trophy, NAME_FONT, color, x, y)
                x += spacing + 150

    def click_trophies(self, mouse_pos):
        x, y = 50, 350
        width = 150
        height = 80
        spacing = 50
        for trophy in self.trophies:
            trophy_rect = pygame.Rect(x, y - 20, width, height)
            if trophy_rect.collidepoint(mouse_pos):
                self.trophies_selected[trophy] = not self.trophies_selected[trophy]
                break
            x += spacing + width

    def click_gobblegum(self, mouse_pos):
        x, y = 75, 700
        spacing = 100
        for i in range(5):
            if (x <= mouse_pos[0] <= x + 140) and (y <= mouse_pos[1] <= y + 140):
                gobblegum = self.gobblegum_names[i]
                self.gobblegums[gobblegum] = False
                all_selected = False
                for key in self.gobblegums:
                    if self.gobblegums[key]:
                        all_selected = True
                if not all_selected:
                    for key in self.gobblegums:
                        self.gobblegums[key] = True
                return gobblegum
            x += 140 + spacing

    def draw_bombs(self):
        x, y = 50, 350
        spacing = 200
        pressed_keys = pygame.key.get_pressed()
        key_mapping = {
            pygame.K_1: "DEPT",
            pygame.K_2: "DRAGON",
            pygame.K_3: "ARM",
            pygame.K_4: "SUPPLY",
            pygame.K_5: "INF",
            pygame.K_6: "TANK",
        }
        for key, location in key_mapping.items():
            if pressed_keys[key] and location not in self.pressed_locations:
                self.pressed_locations.append(location)
        for i, location in enumerate(self.pressed_locations):
            self.draw_text(location, NAME_FONT, WHITE, x + i * spacing, y)

    def handle_click(self, mouse_pos):
        if self.RESET_BUTTON_RECT.collidepoint(mouse_pos):
            self.reset_valves()
            return
        self.click_trophies(mouse_pos)
        x, y = 35, 470
        width = 140
        height = 40
        spacing = 5
        for valve_name in self.locations:
            for i in range(5):
                box_y = y + (i * (spacing + height))
                if (x <= mouse_pos[0] <= x + width) and (box_y <= mouse_pos[1] <= box_y + height):
                    if i == 0:
                        for name in self.selected_states:
                            self.selected_states[name][0] = 0
                        self.selected_states[valve_name][0] = 1
                        if self.selected_states[valve_name][1] == 1:
                            self.selected_states[valve_name][1] = 0
                    elif i == 1:
                        for name in self.selected_states:
                            self.selected_states[name][1] = 0
                        self.selected_states[valve_name][1] = 1
                        if self.selected_states[valve_name][0] == 1:
                            self.selected_states[valve_name][0] = 0
                        self.selected_states[valve_name][2] = 0
                        self.selected_states[valve_name][3] = 0
                        self.selected_states[valve_name][4] = 0
                    else:
                        self.selected_states[valve_name][1] = 0
                        self.selected_states[valve_name][2] = 0
                        self.selected_states[valve_name][3] = 0
                        self.selected_states[valve_name][4] = 0
                        self.selected_states[valve_name][i] = 1
            x += 170

    def display_optimal_solution(self):
        self.results.clear()
        for i in self.valve_logic.return_optimal_solution(self.locations, self.selected_states):
            self.results.append(i)

    def draw_timer(self):
        timer_text = self.timer.get_time()
        self.draw_text(timer_text, TIMER_FONT, WHITE, 1000, 150)
        attempts_text = f"Attempts: {self.timer.get_attempts()}"
        self.draw_text(attempts_text, NAME_FONT, WHITE, 1000, 240)

    def reset(self):
        self.personal_records = []
        self.world_record = []
        self.pressed_locations = []
        self.reset_valves()
        for key in self.gobblegums:
            self.gobblegums[key] = True
        for key in self.trophies_selected:
            self.trophies_selected[key] = False
        return self.selected_states, self.results, self.gobblegums

    def reset_valves(self):
        for key in self.selected_states:
            self.selected_states[key] = [0, 0, 0, 0, 0]
        self.results.clear()

    def update_visual_splits(self):
        self.personal_records = self.timer.get_personal_record()
        self.world_record = self.timer.get_world_record()

    def draw_split_names(self):
        x, y = 25, 75
        for split in self.split_names:
            text = SPLIT_FONT.render(split, True, WHITE)
            text_width = text.get_width()
            self.draw_text(split, SPLIT_FONT, WHITE, x + text_width // 2, y)
            y += 50

    def draw_splits(self):
        x, y = 350, 25
        self.draw_text("World Record", SPLIT_FONT, WHITE, x, y)
        y += 50
        for split in self.world_record:
            if split > 0:
                split = "+" + convert_seconds_to_mins(split)
                self.draw_text(split, SPLIT_FONT, RED, x, y)
            else:
                split = "-" + convert_seconds_to_mins(split)
                self.draw_text(split, SPLIT_FONT, GREEN, x, y)
            y += 50
        y = 25
        x += 250
        self.draw_text("Personal Best", SPLIT_FONT, WHITE, x, y)
        y += 50
        for split in self.personal_records:
            if split > 0:
                split = "+" + convert_seconds_to_mins(split)
                self.draw_text(split, SPLIT_FONT, RED, x, y)
            else:
                split = "-" + convert_seconds_to_mins(split)
                self.draw_text(split, SPLIT_FONT, GREEN, x, y)
            y += 50

    def draw_black_rect(self):
        pygame.draw.rect(self.win, BLACK, (0, 0, 1250, 400))

    def draw_reset_button(self):
        pygame.draw.rect(self.win, BLACK, self.RESET_BUTTON_RECT)
        self.draw_text("RESET VALVES", NAME_FONT, WHITE, self.RESET_BUTTON_RECT.centerx, self.RESET_BUTTON_RECT.centery)

    def draw_gui(self):
        self.draw_black_rect()
        self.draw_trophies()
        self.draw_valve_buttons()
        self.draw_valve_text()
        self.draw_valve_headings()
        self.draw_gobblegums()
        self.draw_timer()
        self.draw_results_box()
        self.draw_splits()
        self.draw_split_names()
        self.draw_reset_button()
