import pygame
from images import *
import time
from logic import *
import json
import logic 


pygame.font.init()
pygame.init()
pygame.display.set_caption("Gorod Krovi Easter Egg")

clock = pygame.time.Clock()
win = pygame.display.set_mode((1250, 850))




GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

STAT_FONT = pygame.font.SysFont("comicsans", 50)
# font = pygame.font.SysFont(None, 30)


valve_logic = logic.ValveLogic("valve.json")

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Define a dictionary to keep track of the selected state for each location
selected_states = {"DEPT": False, "DRAGON": False, "ARM": False, "SUPPLY": False, "INF": False, "TANK": False}

def draw_valve_buttons():
    # Draw valve control buttons
    x, y = 50, 100
    spacing = 60  # Increased spacing between rows
    name_font = pygame.font.SysFont("comicsans", 30)  # Smaller font for location names

    for row, valve_name in enumerate(["DEPT", "DRAGON", "ARM", "SUPPLY", "INF", "TANK"]):
        # Draw valve name with smaller font
        draw_text(valve_name, name_font, BLACK, win, x, y + row * spacing)

        # Draw Green box
        pygame.draw.rect(win, GREEN if selected_states[valve_name] else BLACK, (x + 120, y + row * spacing, 80, 40))

        # Draw cylinder
        pygame.draw.rect(win, GREEN, (x + 220, y + row * spacing, 40, 40))

        # Draw options 1, 2, and 3
        for i in range(3):
            pygame.draw.rect(win, GREEN, (x + 280 + i * 60, y + row * spacing, 40, 40))
            draw_text(str(i + 1), STAT_FONT, BLACK, win, x + 295 + i * 60, y + row * spacing)

def handle_click(mouse_pos):
    # Handle mouse click events
    for row, valve_name in enumerate(["DEPT", "DRAGON", "ARM", "SUPPLY", "INF", "TANK"]):
        # Check if the click occurred on the Green box
        if 100 <= mouse_pos[0] <= 200 and y + row * spacing <= mouse_pos[1] <= y + row * spacing + 40:
            # Toggle the selected state
            selected_states[valve_name] = not selected_states[valve_name]
            return



def draw_gui():
    # Draw all GUI elements
    draw_valve_buttons()
    

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

        # Clear the screen
        win.fill((255, 255, 255))

        # Draw GUI elements
        draw_gui()

        # Update the display
        pygame.display.update()

    pygame.quit()

def handle_click(mouse_pos):
    # Handle mouse click events
    for row, valve_name in enumerate(["DEPT", "DRAGON", "ARM", "SUPPLY", "INF", "TANK"]):
        # Check if the click occurred on the Green box
        if 100 <= mouse_pos[0] <= 200 and 100 + row * 50 <= mouse_pos[1] <= 140 + row * 50:
            # Set the selected state of all valves to False
            for name in selected_states:
                selected_states[name] = False
            # Set the selected state of the clicked valve to True
            selected_states[valve_name] = True
            return


if __name__ == "__main__":
    main()
