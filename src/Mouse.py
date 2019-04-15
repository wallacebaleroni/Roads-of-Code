import pygame
from pygame import Vector2

from util import *
from GameObject import *


class Mouse(GameObject):
    def __init__(self, image, position=Vector2(0, 0), debug=False):
        GameObject.__init__(self, image, position, debug)

    def update(self, dt=0):
        self.screen_pos = Vector2(pygame.mouse.get_pos())
        self.image_rect.center = self.screen_pos

    def get_pos(self):
        return self.position

    def get_screen_pos(self):
        return self.screen_pos

    def toggle_debug(self):
        self.DEBUG = not self.DEBUG

    def reset(self):
        self.set_pos(self.initial_position)
