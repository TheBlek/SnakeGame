import pygame
import numpy as np
import misc
import world_class as world
import warnings

class Layout:

    def __init__(self, label, bg_color=None, is_over_game=False, world=None):
        self.label = label
        self.buttons = np.array([])
        self.labels = np.array([])
        self.is_over_game = is_over_game
        if is_over_game and not world:
            warnings.warn("layout is over game but u didn't passed the world")
        self.world = world
        self.bg_color = bg_color

    def add_button(self, *args, **kwargs):
        self.buttons = np.append(self.buttons, Button(*args, **kwargs))

    def add_label(self, *args, **kwargs):
        self.labels = np.append(self.labels, Label(*args, **kwargs))

    def handle_mouse_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.check_button_click(event)

    def check_button_click(self, mouse_event):
        for button in self.buttons:
            if button.rect.collidepoint(mouse_event.pos):
                try:
                    button.on_click(*button.on_click_data)
                except Exception as e:
                    raise e
                    warnings.warn("button.on_click is empty or args doesn't match signature", RuntimeWarning)

    def update(self, time_elapsed, events):
        if self.is_over_game and self.world:
            self.world.update(time_elapsed)
            if self.world.snake.is_dead:
                misc.put_game_state_to_queue("game_over")
                self.world = world.World()
        self.handle_mouse_events(events)

    def draw(self, win):
        if self.bg_color:
            win.fill(self.bg_color)
        if self.is_over_game and self.world:
            self.world.draw(win)
        for button in self.buttons:
            button.draw(win)
        for label in self.labels:
            label.draw(win)
        pygame.display.update()

class Button:

    def __init__(self, x, y, width, height, label, bg_color, text_color, text_size, on_click, *args):
        self.x = x - width/2
        self.y = y - height/2
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, width, height)

        self.label = label
        self.bg_color = bg_color

        self.on_click = on_click
        self.on_click_data = args

        self.text_color = text_color
        self.text_size = text_size

    def draw(self, win):
        pygame.draw.rect(win, self.bg_color, self.rect)
        font = pygame.font.SysFont('Arial', self.text_size)

        text_sur = font.render(self.label, True, self.text_color)
        text_rect = text_sur.get_rect()
        text_rect.center = (self.x + self.width/2, self.y + self.height/2)
        win.blit(text_sur, text_rect)

class Label:

    def __init__(self, x, y, label, text_size, text_color, bold=False):
        self.x = x
        self.y = y
        self.label = label
        self.text_size = text_size
        self.text_color = text_color
        self.bold = bold

    def draw(self, win):
        font = pygame.font.SysFont('Arial', self.text_size, bold=self.bold)
        text_sur = font.render(self.label, True, self.text_color)
        text_rect = text_sur.get_rect()
        text_rect.center = (self.x, self.y)
        win.blit(text_sur, text_rect)