import pygame
import numpy as np

WIDTH = 800
HEIGHT = 600
ERROR = 0.5

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Turn(Point):

    def __init__(self, x, y, direction):
        super().__init__(x, y)
        self.direction = direction

    def __str__(self):
        return("x = %s; y = %s;" % (self.x, self.y))

class Collision:

    @staticmethod
    def point2rect(point, rect):
        if len(rect) != 4:
            raise ValueError("Rect is not 4-length")

        if (point.x >= rect[0] and point.x <= rect[0] + rect[2] and point.y >= rect[1] and point.y <= rect[1] + rect[3]):
            return True
        return False

    @staticmethod
    def rect2rect(rect1, rect2):
        if len(rect1) != 4 or len(rect2) != 4:
            raise ValueError("Rect is not 4-length")
        point1 = Point(rect1[0], rect1[1])
        point2 = Point(rect1[0] + rect1[2], rect1[1])
        point3 = Point(rect1[0], rect1[1] + rect1[3])
        point4 = Point(rect1[0] + rect1[2], rect1[1] + rect1[3])
        result = Collision.point2rect(point1, rect2) or Collision.point2rect(point2, rect2) or Collision.point2rect(point3, rect2) or Collision.point2rect(point4, rect2)
        return result

class KeyHandler:
    def __init__(self):
        try:
            self.prev_keys = pygame.key.get_pressed()
        except pygame.error as e:
            self.prev_keys = []

    def key_pressed(self, key):
        keys = pygame.key.get_pressed()   
        if keys[key] and not self.prev_keys[key]:
            self.prev_keys = keys
            return True
        self.prev_keys = keys
        return False