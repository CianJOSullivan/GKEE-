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
NAME_FONT = pygame.font.SysFont("Roboto-Black", 30)  # Smaller font for location names
# font = pygame.font.SysFont(None, 30)

# Define a dictionary to keep track of the selected state for each location
selected_states = {"DEPT": [0,0,0,0,0], "DRAGON": [0,0,0,0,0], "ARM": [0,0,0,0,0], "SUPPLY": [0,0,0,0,0], "INF": [0,0,0,0,0], "TANK": [0,0,0,0,0]}
locations = ["DEPT", "DRAGON", "ARM", "SUPPLY", "INF", "TANK"]

# Initialize the ValveLogic class
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
            pygame.draw.rect(win, GREEN if selected_states[valve_name][row]  else BLACK, (x, y + (row * (spacing + height)), width, height))
        x += 170


def draw_valve_headings():
    x, y = 105, 450
    for name in locations:
        draw_text(name, NAME_FONT, BLACK, x , y)
        x += 170


def draw_valve_text():
    x, y = 35, 470
    width = 140
    height = 40
    spacing = 5
    text_options = ["Green", "Cylinder", "1", "2", "3"]
    for valve_name in locations:
        for row in range(5):
            draw_text(text_options[row], NAME_FONT, BLACK if selected_states[valve_name][row]  else WHITE, x + (width//2), y + (row * (spacing + height)) + (height//2))
        x += 170

    
def handle_click(mouse_pos):
    # Handle mouse click events
    x, y = 35, 470
    width = 140
    height = 40
    spacing = 5

    for valve_name  in locations:
        # Check if the click occurred on the Green box
        for i in range(5):
            box_y = y + (i * (spacing + height))
            if (x <= mouse_pos[0] <= x + width) and (box_y <= mouse_pos[1] <= box_y + height):

                if i == 0:
                    for name in selected_states:
                        selected_states[name][0] = 0
                    # Set the selected state of the clicked valve to True
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
    # Draw all GUI elements
    win.fill((240, 240, 240))
    draw_valve_buttons()
    draw_valve_text()
    draw_valve_headings()
    


def main():
    run = True
    while run:
        clock.tick(60)
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse position
                mouse_pos = pygame.mouse.get_pos()
                # Handle mouse click
                handle_click(mouse_pos)

        # Draw GUI elements
        draw_gui()
        pygame.display.update()


    pygame.quit()


if __name__ == "__main__":
    main()
