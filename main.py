import pygame
from images import *
import time
from logic import *
import json

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

selected_states = {"DEPT": [0, 0, 0, 0, 0], "DRAGON": [0, 0, 0, 0, 0], "ARM": [0, 0, 0, 0, 0], "SUPPLY": [0, 0, 0, 0, 0], "INF": [0, 0, 0, 0, 0], "TANK": [0, 0, 0, 0, 0]}
locations = ["DEPT", "DRAGON", "ARM", "SUPPLY", "INF", "TANK"]


# Initialize the ValveLogic class with the path to the JSON file

gobblegum_images = [Reign_Drops, Idle_Eyes, Extra_Credit, Nukes, Abh]
gobblegum_images = [pygame.transform.scale(image, (140, 140)) for image in gobblegum_images]
gobblegum_images_gray = []

for image in gobblegum_images:
    image_gray = image.copy()
    image_gray.fill((45, 45, 45, 255), special_flags=pygame.BLEND_RGBA_MULT)
    gobblegum_images_gray.append(image_gray)
    

gobblegum_names = ["Reign_Drops", "Idle_Eyes", "Extra_Credit", "Nukes", "Abh"]

gobblegums = {"Reign_Drops": True, "Idle_Eyes": True, "Extra_Credit": True, "Nukes": True, "Abh": True}



valve_logic = ValveLogic("valve.json")

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
            pygame.draw.rect(win, GREEN if selected_states[valve_name][row] else BLACK, (x, y + (row * (spacing + height)), width, height))
        x += 170

def draw_valve_headings():
    x, y = 105, 450
    for name in locations:
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
            draw_text(text_options[row], NAME_FONT, BLACK if selected_states[valve_name][row] else WHITE, x + (width // 2), y + (row * (spacing + height)) + (height // 2))
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
        x +=  140 + spacing
        
    
        


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
 

    

def handle_click(mouse_pos):
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

def draw_gui():
    win.fill((240, 240, 240))
    draw_valve_buttons()
    draw_valve_text()
    draw_valve_headings()


    draw_gobblegums()
    


def get_current_state():
    current_state = {}
    for valve_name in locations:
        if selected_states[valve_name][0]:
            for i in range(2, 5):
                if selected_states[valve_name][i]:
                    current_state[valve_name] = f"green-{i-1}"
        elif selected_states[valve_name][1]:
            current_state[valve_name] = "cylinder"
        else:
            for i in range(2, 5):
                if selected_states[valve_name][i]:
                    current_state[valve_name] = str(i - 1)
                    break
    return current_state

def get_changes_required(current_state, best_output):
    """
    Get the changes required to reach the best output from the current state.
    """
    changes_required = {}
    for valve_name, value in best_output.items():
        current_value = current_state.get(valve_name)
        # Remove the "green-" prefix if present in the current state
        if isinstance(current_value, str) and current_value.startswith("green-"):
            current_value = current_value.split("-")[1]
        # Convert string values to integers if necessary
        if isinstance(current_value, str) and current_value.isdigit():
            current_value = int(current_value)
        # Check if the values are different
        if current_value != value:
            changes_required[valve_name] = value
    return changes_required






def main():
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                handle_click(mouse_pos)
                click_gobblegum(mouse_pos)

        # Check for optimal solution if a green light is turned on
        current_state = get_current_state()

        if any("green" in value for value in current_state.values()):
            optimal_solution, best_output = valve_logic.find_optimal_solution(current_state)
            if best_output:
                print("Current State:", current_state)
                print("Best Output:", best_output)
                changes_required = get_changes_required(current_state, best_output)
                print("Changes Required:", changes_required)
                for valve_name, value in changes_required.items():
                    print(f"{valve_name} to {value}")

        draw_gui()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()