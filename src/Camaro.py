import pygame

from metrics import *
from Vehicle import *

class Camaro(Vehicle):
    def __init__(self, position, velocity=(1, 0), debug=False):
        self.image = pygame.image.load("../img/camaro.png")
        self.image_rect = self.image.get_rect()

        Vehicle.__init__(self, self.image, position, velocity, debug)

        self.maxspeed = metric_to_pixel(22)
        self.maxaccel = metric_to_pixel(25)
        self.maxbrake = metric_to_pixel(145)
