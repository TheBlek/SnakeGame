import pygame
import numpy as np
import ui_class as ui
import misc
import world_class

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BACKGROUND = WHITE

class SnakeGame:

    def __init__(self):
        self.game_state = "main_menu"
        self.WIDTH = 800
        self.HEIGHT = 600
        self.ERROR = 0.5
        self.init_layouts()

    def init_layouts(self):
        main_menu_layout = ui.Layout("main_menu", BACKGROUND)
        main_menu_layout.add_label(self.WIDTH/2, 50, "Snake Game", 50, BLACK, bold=True)
        main_menu_layout.add_button(self.WIDTH/2, self.HEIGHT/2, self.WIDTH/2, 90, "Play", BACKGROUND, BLACK, 30, misc.put_game_state_to_queue, "game")

        game_layout = ui.Layout("game", BACKGROUND, True, world_class.World())

        game_over_layout = ui.Layout("game_over", BACKGROUND)
        game_over_layout.add_label(self.WIDTH/2, self.HEIGHT/2, "YOU DIED", 90, RED, bold=True)
        game_over_layout.add_button(self.WIDTH/2, self.HEIGHT/2 + 90, self.WIDTH/2, 90, "Play again?", BACKGROUND, BLACK, 30, misc.put_game_state_to_queue, "game")

        self.layouts = {"main_menu" : main_menu_layout, "game": game_layout, "game_over": game_over_layout}

    def change_game_state(self, new_state):
        if self.game_state != new_state:
            self.game_state = new_state

    def update_game(self, win):
        events = pygame.event.get()
        time_elapsed = pygame.time.get_ticks() - self.time
        self.time = pygame.time.get_ticks()
        layout = self.layouts[self.game_state]

        layout.update(time_elapsed, events)
        layout.draw(win)

        for event in events:
            if event.type == pygame.USEREVENT+1:
                self.change_game_state( event.new_state )
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False
                break

    def start_game(self):
        pygame.init()
        win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Snake game by @dDevyce v0.1")

        self.run = True
        self.time = pygame.time.get_ticks()

        while self.run:
            self.update_game(win)