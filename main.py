import pygame


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



win.fill((0, 0, 0))
run = True
while run:
    clock.tick(60)


    # win.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False





    pygame.display.update()

pygame.quit()

