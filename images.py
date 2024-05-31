import pygame 

# Load the image
Abh = pygame.image.load('images/Anywhere_But_Here.jpeg')
Nukes = pygame.image.load('images/Dead_of_Nuclear_Winter_GobbleGum_BO3.jpeg')
Extra_Credit = pygame.image.load('images/Extra_Credit.jpeg')
Idle_Eyes = pygame.image.load('images/Idle_Eyes_GobbleGum_BO3.jpeg')
Reign_Drops = pygame.image.load('images/Reign_Drops_GobbleGum_BO3.jpeg')
Shopping_Free = pygame.image.load('images/Shopping_Free_GobbleGum_BO3.jpeg')

def draw_valve_buttons():
    x, y = 35, 520
    width = 140
    height = 32
    spacing = 5

    for col in locations:
        for row in range(5):
            pygame.draw.rect(win, GREEN if selected_states[valve_name] else BLACK, (x, y + (row * (spacing + height)), width, height))
        x += 150