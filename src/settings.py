import pygame

pygame.font.init()

WIN_WIDTH, WIN_HEIGHT = 1250, 850

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


STAT_FONT = pygame.font.SysFont("Roboto-Black", 50)
NAME_FONT = pygame.font.SysFont("Roboto-Black", 30)
TIMER_FONT = pygame.font.SysFont("Roboto-Black", 250)
SPLIT_FONT = pygame.font.SysFont("Roboto-Black", 40)


def convert_seconds_to_mins(seconds):
    seconds = abs(seconds)
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    if seconds > 59:
        return f"{minutes:01}:{remaining_seconds:02}"
    else:
        return f"{seconds}"