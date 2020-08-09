import pygame
import numpy as np
import snake_class as snake
import food_class as food
import misc

class World:

    def __init__(self):
        self.snake = snake.Snake()
        self.food = food.Food()
        self.key_handler = misc.KeyHandler()

    def update(self, time_elapsed):
        self.snake.update(time_elapsed, self)
        self.check_snake_food_collision()

    def draw(self, win):
        self.snake.draw(win)
        self.food.draw(win)

    def spawn_new_food(self):
        self.food = food.Food()

    def check_snake_food_collision(self):
        head_rect = self.snake.get_head_top_rect()
        if misc.Collision.rect2rect(head_rect, self.food.rect):
            self.snake.eat()
            self.spawn_new_food()