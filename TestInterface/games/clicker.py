import pygame
from pygame.locals import *

def main(score_data):
    print(score_data)
    dp = init_window()
    running = True
    while (running):
        for e in pygame.event.get():
            on_event(e)
        draw(dp):
    return score_data

def init_window():
    pygame.init()
    return pygame.display.set_mode((400, 400), pygame.HWSURFACE | pygame.DOUBLEBUF)

def on_event(e):
    if e.type == pygame.QUIT:
        running = False

def draw(dp):
    pass