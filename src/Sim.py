import pygame
from pygame import Vector2

from util import *
from GameObject import *
from Vehicle import *
from Camaro import *


class Sim:
    def __init__(self, size):
        # Initializes pygame
        pygame.init()

        # Initializes game variables
        self.DEBUG = False

        # Initializes screen
        self.screen = pygame.display.set_mode(size)
        self.screen_size = size

        # Sets screen title
        pygame.display.set_caption("Roads of Code")

        # Initializes time variables
        self.last_time = 0
        self.dt_multiplier = 1
        self.dt_mult_pace = 0.25
        self.dt_step = False
        self.dt_manual_max = 0.5
        self.dt_manual = self.dt_manual_max
        self.dt_manual_pace = 0.1
        self.pace_changed = False

        # Creates running flag
        self.run = True

        # Creates mouse object
        self.mouse = GameObject(pygame.image.load("../img/dot.png"))

        # Creates game objects dict
        self.game_objects = {'vehicles': [], 'mouse': [self.mouse]}

        # Initializes centered game object
        self.tracking_game_object = None

        # Loads initial game objects
        self.load_scenary()

    def load_scenary(self):
        # Initializes single vehicle
        position = Vector2(self.screen_size[0] / 2, self.screen_size[1] / 2)
        vehicle = Camaro(position, debug=self.DEBUG)
        vehicle.set_velocity(Vector2(0, 0))
        vehicle.set_accel(Vector2(0, 0))

        self.tracking_game_object = vehicle
        self.game_objects['vehicles'].append(vehicle)

        position = Vector2(300, 300)
        vehicle = Camaro(position, debug=self.DEBUG)
        vehicle.set_velocity(Vector2(0, 0))
        vehicle.set_accel(Vector2(0, 0))

        self.game_objects['vehicles'].append(vehicle)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_MINUS:  # Key -
                    # Decreases the lenght in time of each pace until zero
                    if self.dt_multiplier > 0:
                        self.dt_multiplier -= self.dt_mult_pace
                    # After reaching zero, the manual pace will be decreased until zero
                    else:
                        if self.dt_manual > 0:
                            self.dt_manual -= self.dt_manual_pace
                    self.pace_changed = True
                if event.key == pygame.K_EQUALS:  # Key +
                    if self.dt_manual < self.dt_manual_max:
                        self.dt_manual += self.dt_manual_pace
                    else:
                        self.dt_multiplier += self.dt_mult_pace
                    self.pace_changed = True
                if event.key == pygame.K_p:  # Key p
                    self.dt_step = True
                if event.key == pygame.K_BACKQUOTE:  # Key "
                    self.toggle_debug()
                if event.key == pygame.K_r:  # Key r
                    self.reset_sim()

    def reset_sim(self):
        for vehicle in self.game_objects['vehicles']:
            vehicle.reset()

    def toggle_debug(self):
        # Toggle debug for itself and every debuggable object
        self.DEBUG = not self.DEBUG

        for vehicle in self.game_objects['vehicles']:
            vehicle.toggle_debug()

    def update(self):
        # Gets dt
        dt = self.update_dt()

        # Updates mouse object
        self.mouse.set_pos(pygame.mouse.get_pos())
        self.mouse.update()

        # Updates vehicles
        for vehicle in self.game_objects['vehicles']:
            vehicle.update(dt, self.game_objects)
        print(self.game_objects['vehicles'][0].get_pos())
        print(self.game_objects['vehicles'][1].get_pos())
        # Updates background
        self.update_background()

    def update_dt(self):
        # Updates dt
        current_time = pygame.time.get_ticks() / 1000
        dt = current_time - self.last_time

        dt = dt * self.dt_multiplier

        if self.dt_step:
            dt = self.dt_manual
            self.dt_step = False

        self.last_time = current_time

        return dt

    def update_background(self):
        #return
        if self.tracking_game_object is not None:
            center_offset = self.tracking_game_object.position - self.screen_size

            for key in self.game_objects.keys():
                if key == 'vehicles':
                    for vehicle in self.game_objects[key]:
                        if vehicle != self.tracking_game_object:
                            vehicle.set_pos(vehicle.get_pos() - center_offset)

    def draw(self):
        # Draws background
        self.screen.fill((0, 0, 0))

        # Draws mouse
        if self.DEBUG:
            self.game_objects['mouse'][0].draw(self.screen)

        # Draws vehicles
        for vehicle in self.game_objects['vehicles']:
            vehicle.draw(self.screen)

    def loop(self):
        # Initializes time variables
        self.last_time = pygame.time.get_ticks() / 1000

        while self.run:
            self.handle_events()

            self.update()
            self.draw()

            pygame.display.flip()
