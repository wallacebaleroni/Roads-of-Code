import pygame
from src.Vehicle import Vehicle


class Sim:
    screen = None
    screen_size = None
    run = True
    interval = 0

    def __init__(self, size, DEBUG):
        # Initializes game variables
        self.DEBUG = DEBUG
        self.vehicles = []

        # Initializes pygame
        pygame.init()

        # Initializes screen
        self.screen = pygame.display.set_mode(size)
        self.screen_size = size

        # Sets screen title
        pygame.display.set_caption("Roads of Code")

        # Loads images
        self.load_images()

    def load_images(self):
        self.image_vehicle = pygame.image.load("../img/car.png")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def update(self, dt):
        for vehicle in self.vehicles:
            vehicle.update(dt)

    def draw(self):
        self.screen.fill((0, 0, 0))

        for vehicle in self.vehicles:
            vehicle.draw(self.screen)

    def loop(self):
        # Initializates position and vehicle
        position = [self.screen_size[0] / 2, self.screen_size[1] / 2]
        vehicle = Vehicle(self.image_vehicle, position, debug=self.DEBUG)
        vehicle.set_speed((0, 0))
        vehicle.set_accel((0, 0))

        self.vehicles.append(vehicle)

        # Initializates time variables
        dt = 0
        time_initial = pygame.time.get_ticks() / 1000

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
        meters_per_pixel = 0.13

        vehicle = self.vehicles[0]

        speed_text = "vSpeed: %0.2f km/h" % (vehicle.get_speed()[1] * meters_per_pixel * 3.6)
        accel_text = "vAccel: %0.2f km/h" % (vehicle.get_accel()[1] * meters_per_pixel * 3.6)

        print(speed_text + "   " + accel_text)
