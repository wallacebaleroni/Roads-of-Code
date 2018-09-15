import pygame

from src.Vehicle import Vehicle

class Camaro(Vehicle):
    def __init__(self, position, velocity=(1, 0), debug=False):
        vehicle_image = pygame.image.load("../img/camaro.png")

        Vehicle.__init__(self, vehicle_image, position, velocity, debug)

        self.maxspeed = self.metric_to_pixel(22)
        self.maxaccel = self.metric_to_pixel(25)
        self.maxbrake = -self.metric_to_pixel(145)
