import pygame
import numpy as np

WIDTH = 800
HEIGHT = 600
ERROR = 0.5

class Food:

    def __init__(self, x=-1, y=-1):
        if x == -1:
            x = np.random.random() * WIDTH
        if y == -1:
            y = np.random.random() * HEIGHT

        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.rect = (x, y, self.width, self.height)
        self.color = (255, 0, 0)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)