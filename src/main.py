import pygame
from images import *
from logic import *
from timer import Timer

import time
import json
from server import Server

server = Server()

pygame.font.init()
pygame.init()
pygame.display.set_caption("Gorod Krovi Easter Egg")

icon = Shopping_Free
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
win = pygame.display.set_mode((1250, 850))

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

STAT_FONT = pygame.font.SysFont("Roboto-Black", 50)
NAME_FONT = pygame.font.SysFont("Roboto-Black", 30)
TIMER_FONT = pygame.font.SysFont("Roboto-Black", 250)
SPLIT_FONT = pygame.font.SysFont("Roboto-Black", 40)

RESET_BUTTON_RECT = pygame.Rect(1050, 420, 170, 40)

selected_states = {"DEPT": [0, 0, 0, 0, 0], "DRAGON": [0, 0, 0, 0, 0], "ARM": [
    0, 0, 0, 0, 0], "SUPPLY": [0, 0, 0, 0, 0], "INF": [0, 0, 0, 0, 0], "TANK": [0, 0, 0, 0, 0]}
locations = ["DEPT", "DRAGON", "ARM", "SUPPLY", "INF", "TANK"]

results = []
personal_record = []
world_record = []

split_names = ["Flight 1", "Flight 2", "Start Trophy", "Start Boss", "Finish"]

gobblegum_images = [Reign_Drops, Idle_Eyes, Extra_Credit, Nukes, Shopping_Free]
gobblegum_images = [pygame.transform.scale(
    image, (140, 140)) for image in gobblegum_images]
gobblegum_images_gray = []

for image in gobblegum_images:
    image_gray = image.copy()
    image_gray.fill((45, 45, 45, 255), special_flags=pygame.BLEND_RGBA_MULT)
    gobblegum_images_gray.append(image_gray)

gobblegum_names = ["Reign_Drops", "Idle_Eyes",
                   "Extra_Credit", "Nukes", "Shopping_Free"]
gobblegums = {"Reign_Drops": True, "Idle_Eyes": True,
              "Extra_Credit": True, "Nukes": True, "Shopping_Free": True}

trophies = ["Spawn", "Eyebeam", "Tank", "Toilet", "Dragon S", "Bunker"]
trophies_selected = {trophy: False for trophy in trophies}

valve_logic = ValveLogic("../data/valve.json")
timer = Timer()

def draw_text(text, font, color, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    win.blit(textobj, textrect)

def draw_valve_buttons():
    x, y = 35, 470
    width = 140
    height = 40
    spacing = 5
    for valve_name in locations:
        for row in range(5):
            pygame.draw.rect(win, GREEN if selected_states[valve_name][row] else BLACK, (
                x, y + (row * (spacing + height)), width, height))
        x += 170

def draw_results_box():
    pygame.draw.rect(win, BLACK, (1050, 470, 170, 220))
    x, y = 1050, 470
    for result in results:
        text = NAME_FONT.render(result, True, WHITE)
        text_width = text.get_width()
        draw_text(result, NAME_FONT, WHITE, x + 10 + (text_width // 2), y + 20)
        y += 35

def draw_valve_headings():
    x, y = 105, 450
    headings = locations.copy()
    headings.append("RESULTS")
    for name in headings:
        draw_text(name, NAME_FONT, BLACK, x, y)
        x += 170

def draw_valve_text():
    x, y = 35, 470
    width = 140
    height = 40
    spacing = 5
    text_options = ["Green", "Cylinder", "1", "2", "3"]
    for valve_name in locations:
        for row in range(5):
            draw_text(text_options[row], NAME_FONT, BLACK if selected_states[valve_name][row]
                      else WHITE, x + (width//2), y + (row * (spacing + height)) + (height//2))
        x += 170

def draw_gobblegums():
    x, y = 75, 700
    spacing = 100
    for val, image in enumerate(gobblegum_images):
        name = gobblegum_names[val]
        if gobblegums[name] == False:
            win.blit(gobblegum_images_gray[val], (x, y))
        else:
            win.blit(image, (x, y))
        x += 140 + spacing


def draw_trophies():
    if not all(trophies_selected.values()):  
        x, y = 50, 350
        spacing = 200
        for trophy in trophies:
            color = GREEN if trophies_selected[trophy] else RED
            
            text_surface = NAME_FONT.render(trophy, True, WHITE)
            text_rect = text_surface.get_rect(topleft=(x - 47, y - 10))  
            text_rect.width += 20  
            text_rect.height += 20
            #pygame.draw.rect(win, (0, 0, 0, 0), text_rect)  

            draw_text(trophy, NAME_FONT, color, x, y)
            x += spacing


def click_gobblegum(mouse_pos):
    x, y = 75, 700
    spacing = 100
    for i in range(5):
        if (x <= mouse_pos[0] <= x + 140) and (y <= mouse_pos[1] <= y + 140):
            gobblegum = gobblegum_names[i]
            gobblegums[gobblegum] = False
            all_selected = False
            for key in gobblegums:
                if gobblegums[key] == True:
                    all_selected = True
            if not all_selected:
                for key in gobblegums:
                    gobblegums[key] = True
            return gobblegum
        x += 140 + spacing

pressed_locations = [] # Move the list outside of draw_bombs()

def draw_bombs():
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
        if pressed_keys[key] and location not in pressed_locations:
            pressed_locations.append(location)  # Add only if not already present

    for i, location in enumerate(pressed_locations):
        draw_text(location, NAME_FONT, WHITE, x + i * spacing, y)

def click_trophies(mouse_pos):
    x, y = 50, 350
    spacing = 200
    padding = 10

    for trophy in trophies:
        text_surface = NAME_FONT.render(trophy, True, WHITE)
        text_width, text_height = text_surface.get_size()

        # Create larger rectangle for click detection
        text_rect = text_surface.get_rect(topleft=(x - padding, y - text_height // 2 - padding))
        text_rect.width += 2 * padding
        text_rect.height += 2 * padding

        if text_rect.collidepoint(mouse_pos):
            trophies_selected[trophy] = not trophies_selected[trophy]
            break  

        x += spacing  


def handle_click(mouse_pos):
    if RESET_BUTTON_RECT.collidepoint(mouse_pos):
        reset_valves()
        return
    click_trophies(mouse_pos)
    x, y = 35, 470
    width = 140
    height = 40
    spacing = 5
    for valve_name in locations:
        for i in range(5):
            box_y = y + (i * (spacing + height))
            if (x <= mouse_pos[0] <= x + width) and (box_y <= mouse_pos[1] <= box_y + height):
                if i == 0:
                    for name in selected_states:
                        selected_states[name][0] = 0
                    selected_states[valve_name][0] = 1
                    if selected_states[valve_name][1] == 1:
                        selected_states[valve_name][1] = 0
                elif i == 1:
                    for name in selected_states:
                        selected_states[name][1] = 0
                    selected_states[valve_name][1] = 1
                    if selected_states[valve_name][0] == 1:
                        selected_states[valve_name][0] = 0
                    selected_states[valve_name][2] = 0
                    selected_states[valve_name][3] = 0
                    selected_states[valve_name][4] = 0
                else:
                    selected_states[valve_name][1] = 0
                    selected_states[valve_name][2] = 0
                    selected_states[valve_name][3] = 0
                    selected_states[valve_name][4] = 0
                    selected_states[valve_name][i] = 1
        x += 170

def display_optimal_solution():
    results.clear()
    for i in valve_logic.return_optimal_solution(locations, selected_states):
        results.append(i)

def draw_timer():
    timer_text = timer.get_time()
    draw_text(timer_text, TIMER_FONT, WHITE, 1000, 150)

    attempts_text = f"Attempts: {timer.get_attempts()}"
    draw_text(attempts_text, NAME_FONT, WHITE, 1000, 240)

def reset():
    global personal_record, world_record, pressed_locations
    personal_record = []
    world_record = []
    pressed_locations = []
    reset_valves()

    for key in gobblegums:
        gobblegums[key] = True

    for key in trophies_selected:   
        trophies_selected[key] = False
    return selected_states, results, gobblegums
    

def reset_valves():
    for key in selected_states:
        selected_states[key] = [0, 0, 0, 0, 0]
    results.clear()

def update_visual_splits():
    global personal_record, world_record
    personal_record = timer.get_personal_record()
    world_record = timer.get_world_record()

def draw_split_names():
    x, y = 25, 75
    for split in split_names:
        text = SPLIT_FONT.render(split, True, WHITE)
        text_width = text.get_width()
        draw_text(split, SPLIT_FONT, WHITE, x + text_width // 2, y)
        y += 50

def convert_seconds_to_mins(seconds):
    seconds = abs(seconds)
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    if seconds > 59:
        return f"{minutes:01}:{remaining_seconds:02}"
    else:
        return f"{seconds}"

def draw_splits():
    x, y = 350, 25
    draw_text("World Record", SPLIT_FONT, WHITE, x, y)
    y += 50
    for split in world_record:
        if split > 0:
            split = "+" + convert_seconds_to_mins(split)
            draw_text(split, SPLIT_FONT, RED, x, y)
        else:
            split = "-" + convert_seconds_to_mins(split)
            draw_text(split, SPLIT_FONT, GREEN, x, y)
        y += 50
    y = 25
    x += 250
    draw_text("Personal Best", SPLIT_FONT, WHITE, x, y)
    y += 50
    for split in personal_record:
        if split > 0:
            split = "+" + convert_seconds_to_mins(split)
            draw_text(split, SPLIT_FONT, RED, x, y)
        else:
            split = "-" + convert_seconds_to_mins(split)
            draw_text(split, SPLIT_FONT, GREEN, x, y)
        y += 50

def draw_black_rect():
    pygame.draw.rect(win, BLACK, (0, 0, 1250, 400))

def draw_reset_button():
    pygame.draw.rect(win, BLACK, RESET_BUTTON_RECT)
    draw_text("RESET VALVES", NAME_FONT, WHITE, RESET_BUTTON_RECT.centerx, RESET_BUTTON_RECT.centery)

def update_game_state(d):
    global selected_states, trophies_selected, results, world_record, personal_record, pressed_locations
    try:
        json_data = json.loads(d)
        print(f"Unpacked JSON data: {json_data}")
        selected_states = json_data["selected_states"]
        trophies_selected = json_data["trophies_selected"]
        timer.set_splits(json_data["splits"])
        timer.running = json_data["running"]
        results = json_data["results"]
        world_record = json_data["world_record"]
        personal_record = json_data["personal_record"]
        pressed_locations = json_data["pressed_locations"]

        timer.wr_difference = json_data["wr_diff"]
        timer.pr_difference = json_data["pr_diff"]
        timer.finished = json_data["finished"]
        timer.start_time = json_data["start_time"]
        
    except json.JSONDecodeError:
        print("Failed to decode JSON data")



def send_info():
    global world_record, personal_record, results
    data_to_send = {
        "selected_states": selected_states,
        "trophies_selected": trophies_selected,
        "splits": timer.get_splits(),
        "results": results,
        "world_record": world_record,
        "personal_record": personal_record,
        "running":timer.running ,
        "pressed_locations":pressed_locations,
       
        

        "wr_diff":timer.wr_difference ,
        "pr_diff":timer.pr_difference,
        "finished":timer.finished ,
        "start_time":timer.start_time 
        

    }
    json_data = json.dumps(data_to_send)
    return json_data


def draw_gui():
    draw_black_rect()
    draw_trophies()
    draw_valve_buttons()
    draw_valve_text()
    draw_valve_headings()
    draw_gobblegums()
    draw_timer()
    draw_results_box()
    draw_splits()
    draw_split_names()
    draw_reset_button()
       
    
    

def main():
    run = True
    while run:
        clock.tick(60)
        win.fill((200, 200, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                handle_click(mouse_pos)
                click_gobblegum(mouse_pos)
                display_optimal_solution()
                server.broadcast_message(send_info())
            elif event.type == pygame.KEYDOWN:
                timer.get_input(event)
                update_visual_splits()
                server.broadcast_message(send_info())
                if event.key == pygame.K_RETURN:
                    reset()

        data = server.handle_connections()
        if data:
            update_game_state(data)
        draw_gui()
        if all(trophies_selected.values()):
            draw_bombs()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()