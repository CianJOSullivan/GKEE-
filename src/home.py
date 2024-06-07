import pygame
from main import main

pygame.init()

WIN_WIDTH, WIN_HEIGHT = 1250, 850
BUTTON_WIDTH, BUTTON_HEIGHT = 250, 250
BUTTON_MARGIN = 50
BUTTON_X_POSITIONS = [150, 450, 750]
BUTTON_Y_POSITION = WIN_HEIGHT // 2 - BUTTON_HEIGHT // 2
TEXT_COLOR = (255, 255, 255)

IMAGE_PATHS = [
    "../images/gk.png",       
    "../images/origins.png",  
    "../images/shadows.png"   
]

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Easter Egg Guide")

def load_and_scale_image(path, width, height):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (width, height))

images = [load_and_scale_image(path, BUTTON_WIDTH, BUTTON_HEIGHT) for path in IMAGE_PATHS]

def draw_images():
    for idx, img in enumerate(images):
        x = BUTTON_X_POSITIONS[idx]
        win.blit(img, (x, BUTTON_Y_POSITION))

def draw_text(text, x, y, font_size=48):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x, y))
    win.blit(text_surface, text_rect)

def main_home():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for idx, x in enumerate(BUTTON_X_POSITIONS):
                    if (x <= mouse_x <= x + BUTTON_WIDTH
                        and BUTTON_Y_POSITION <= mouse_y <= BUTTON_Y_POSITION + BUTTON_HEIGHT):
                        print(f"Map {idx + 1} Selected")
                        if idx == 0:
                            main()
                        elif idx == 1:
                            print("Map 2 Placeholder Selected")
                        elif idx == 2:
                            print("Map 3 Placeholder Selected")
                        running = False

        win.fill((0, 0, 0))  
        draw_text("Welcome to ConsoleSpeed", WIN_WIDTH // 2, 100)
        draw_images()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main_home()
