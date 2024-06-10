import pygame
from images import *

from settings import *
from gorod_krovi import GorodKrovi

pygame.init()
pygame.display.set_caption("Gorod Krovi Easter Egg")

icon = Shopping_Free
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

gk = GorodKrovi(win)


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
                gk.handle_click(mouse_pos)
                gk.click_gobblegum(mouse_pos)
                gk.display_optimal_solution()
            elif event.type == pygame.KEYDOWN:
                gk.timer.get_input(event)
                gk.update_visual_splits()
                if event.key == pygame.K_RETURN:
                    gk.reset()

        gk.draw_gui()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
