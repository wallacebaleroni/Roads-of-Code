import pygame
from pygame import Vector2

from src.metrics import *
from src.GameObject import GameObject
from src.Camaro import Camaro


class Sim:
    interval = 0

    def __init__(self, size, debug):
        # Initializes pygame
        pygame.init()

        # Initializes game variables
        self.DEBUG = debug
        self.vehicles = []

        # Initializes screen
        self.screen = pygame.display.set_mode(size)
        self.screen_size = size

        # Sets screen title
        pygame.display.set_caption("Roads of Code")

        # Creates running flag
        self.run = True

        # Creates mouse object
        self.mouse = GameObject(pygame.image.load("../img/dot.png"))

        # Creates tracked objects dict
        self.tracked_objects = {'vehicles': self.vehicles, 'mouse': self.mouse}

        # Initializes single vehicle
        position = Vector2(self.screen_size[0] / 2, self.screen_size[1] / 2)
        vehicle = Camaro(position, debug=self.DEBUG)
        vehicle.set_velocity(Vector2(0, 0))
        vehicle.set_accel(Vector2(0, 0))

        self.vehicles.append(vehicle)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def update(self, dt):
        # Updates mouse object
        self.mouse.set_pos(pygame.mouse.get_pos())
        self.mouse.update()

        # Updates vehicles
        for vehicle in self.vehicles:
            vehicle.update(dt, self.tracked_objects)

    def draw(self):
        # Draws background
        self.screen.fill((0, 0, 0))

        # Draws mouse
        self.mouse.draw(self.screen)

        # Draws vehicles
        for vehicle in self.vehicles:
            vehicle.draw(self.screen)

    def loop(self):
        # Initializes time variables
        time_initial = pygame.time.get_ticks() / 1000
        dt = 0

        while self.run:
            self.handle_events()

            self.update(dt)
            self.draw()

            pygame.display.flip()

            time_final = pygame.time.get_ticks() / 1000
            dt = time_final - time_initial
            time_initial = time_final

            if self.DEBUG:
                self.get_metrics()

    def get_metrics(self):
        vehicle = self.vehicles[0]

        speed_text = "Velocity: %0.2f km/h" % (pixel_to_metric(Vector2(vehicle.get_velocity()).length()) * 3.6)
        accel_text = "Accel: %0.2f km/h" % (pixel_to_metric(Vector2(vehicle.get_accel()).length()) * 3.6)

        print(speed_text + "   " + accel_text)
