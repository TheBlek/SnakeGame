import pygame
import numpy as np
import misc

WIDTH = 800
HEIGHT = 600
ERROR = 0.5

D_UP = 1
D_DOWN = -1
D_LEFT = 2
D_RIGHT = -2

class Node:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def __str__(self):
        return "x = {self.x}, y = {self.y}\n"

class Snake:

    def __init__(self, x=-1, y=-1):
        if x == -1:
            x = np.random.random() * WIDTH
        if y == -1:
            y = np.random.random() * HEIGHT
        self.x = x
        self.y = y
        self.speed = 100
        self.color = (0, 255, 0)
        self.node_width = 20
        self.node_height = 20
        self.head = Node(x, y, D_UP)
        self.last = self.head
        self.turns = np.array([])

    def move(self, time_elapsed):
        time_elapsed /= 1000
        if self.head.direction == D_UP:
            self.head.y -= self.speed * time_elapsed
        elif self.head.direction == D_RIGHT:
            self.head.x += self.speed * time_elapsed
        elif self.head.direction == D_DOWN:
            self.head.y += self.speed * time_elapsed
        elif self.head.direction == D_LEFT: 
            self.head.x -= self.speed * time_elapsed

        if self.head == self.last:
            return

        if self.last.direction == D_UP:
            self.last.y -= self.speed * time_elapsed
        elif self.last.direction == D_RIGHT:
            self.last.x += self.speed * time_elapsed
        elif self.last.direction == D_DOWN:
            self.last.y += self.speed * time_elapsed
        elif self.last.direction == D_LEFT: 
            self.last.x -= self.speed * time_elapsed
        
        self.check_last_turn()

    def is_out_of_borders(self):
        if self.head.x + self.node_width > WIDTH  or self.head.y + self.node_height > HEIGHT or self.head.x < 0 or self.head.y < 0:
            return True
        return False

    def check_last_turn(self):
        if len(self.turns) != 0:
            dx = abs(self.last.x - self.turns[0].x)
            dy = abs(self.last.y - self.turns[0].y)
            if dx < ERROR and dy < ERROR:
                self.last.direction = self.turns[0].direction
                self.turns = self.turns[1:]

    def get_head_top_rect(self):
        head_rect = (self.head.x, self.head.y, 0, 0)
        
        if self.head.direction == D_UP:
            head_rect = (self.head.x, self.head.y - ERROR, self.node_width, 0)
        elif self.head.direction == D_RIGHT:
            head_rect = (self.head.x + self.node_width + ERROR, self.head.y, 0, self.node_height)
        elif self.head.direction == D_DOWN:
            head_rect = (self.head.x, self.head.y + self.node_height + ERROR, self.node_width, 0)
        elif self.head.direction == D_LEFT: 
            head_rect = (self.head.x - ERROR, self.head.y, 0, self.node_height)

        return head_rect

    def eat(self):
        self.add_node()

    def is_head_self_collision(self):
        if len(self.turns) == 0:
            return False

        head_rect = self.get_head_top_rect()       

        for i in range(len(self.turns) - 1):
            x = min(self.turns[i].x, self.turns[i + 1].x)
            y = min(self.turns[i].y, self.turns[i + 1].y)
            dx = abs(self.turns[i].x - self.turns[i + 1].x)
            dy = abs(self.turns[i].y - self.turns[i + 1].y)
            if misc.Collision.rect2rect(head_rect, (x, y, dx + self.node_width, dy + self.node_height)):
                return True

        x = min(self.turns[0].x, self.last.x)
        y = min(self.turns[0].y, self.last.y)
        dx = abs(self.turns[0].x - self.last.x)
        dy = abs(self.turns[0].y - self.last.y)
        return  misc.Collision.rect2rect(head_rect, (x, y, dx + self.node_width, dy + self.node_height))

    def add_node(self):
        x, y = 0, 0
        if self.last.direction == D_UP:
            y = 1
        elif self.last.direction == D_LEFT:
            x = 1
        elif self.last.direction == D_RIGHT:
            x = -1
        elif self.last.direction == D_DOWN:
            y = -1
        x = self.last.x + x * self.node_width
        y = self.last.y + y * self.node_height
        self.last = Node(x, y, self.last.direction)

    @staticmethod
    def draw_rect(win, start_point, end_point, width, height, color):
        x = min(start_point.x, end_point.x)
        y = min(start_point.y, end_point.y)
        dx = max(start_point.x, end_point.x) - min(start_point.x, end_point.x)
        dy = max(start_point.y, end_point.y) - min(start_point.y, end_point.y)
        rect = (x, y, dx + width, dy + height)
        pygame.draw.rect(win, color, rect)

    def draw(self, win):
        if len(self.turns) == 0:
            Snake.draw_rect(win, self.head, self.last, self.node_width, self.node_height, self.color)
        else:
            Snake.draw_rect(win, self.head, self.turns[-1], self.node_width, self.node_height, self.color)
            for i in range(len(self.turns) - 1):
                Snake.draw_rect(win, self.turns[i], self.turns[i + 1], self.node_width, self.node_height, self.color)
            Snake.draw_rect(win, self.turns[0], self.last, self.node_width, self.node_height, self.color)

    def turn(self, direction):
        if self.head.direction != direction:
            self.head.direction = direction
            if self.head != self.last:
                self.turns = np.append(self.turns, misc.Turn(self.head.x, self.head.y, direction))

    def handle_input(self, key_handler):
        keys = pygame.key.get_pressed()
        head = self.head
        direction = head.direction
        if keys[pygame.K_LEFT] and (head.direction != -D_LEFT):
            direction = D_LEFT
        elif keys[pygame.K_RIGHT] and (head.direction != -D_RIGHT):
            direction = D_RIGHT
        elif keys[pygame.K_UP] and (head.direction != -D_UP):
            direction = D_UP
        elif keys[pygame.K_DOWN] and (head.direction != -D_DOWN):
            direction = D_DOWN
        if key_handler.key_pressed(pygame.K_SPACE):
            self.add_node()
        self.turn(direction)

    def update(self, time_elapsed, world):
        self.handle_input(world.key_handler)
        self.move(time_elapsed)
        if (self.is_head_self_collision() or self.is_out_of_borders()):
            pygame.event.post(pygame.event.Event(pygame.QUIT))