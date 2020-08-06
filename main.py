import pygame
import numpy as np
import world_class as world

WIDTH = 800
HEIGHT = 600
ERROR = 0.5

D_UP = 1
D_DOWN = -1
D_LEFT = 2
D_RIGHT = -2

def redraw(win, world):

    win.fill((255, 255, 255))
    world.draw(win)
    pygame.display.update()

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake game by @dDevyce v0.1")

def main():
    run = True
    world_inst = world.World()

    time = pygame.time.get_ticks()
    while run:
        time_elapsed = pygame.time.get_ticks() - time
        time = pygame.time.get_ticks()
        world_inst.update(time_elapsed)
        redraw(win, world_inst)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                break

main()