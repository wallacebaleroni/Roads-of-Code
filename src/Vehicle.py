from src.aux_ops import *
import pygame


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, position, speed=(1, 0), debug=False):
        pygame.sprite.Sprite.__init__(self)

        # Loads image
        self.image = image
        self.rotated_image = image

        # Gets image and duplay rects
        self.rect = self.image.get_rect()
        self.area = pygame.display.get_surface().get_rect()

        # Sets debug option and initializes debug lines used to show the vectors acting on the vehicle
        self.DEBUG = debug
        self.debug_lines = []

        # Basic forces
        self.position = position
        self.velocity = speed
        self.accel = (0, 0)

        self.maxspeed = self.metric_to_pixel(22)
        self.maxaccel = self.metric_to_pixel(25)
        self.maxbrake = -self.metric_to_pixel(145)

        # Initializes obstacle list
        self.near_obstacles = []

        # Initializes future path rect
        self.generate_future_path_rect()

    def update(self, dt):
        # Applies seeking behavior
        self.apply_force(self.seek(pygame.mouse.get_pos()))
        self.brake()

        # Updates speed and position
        self.velocity = (self.velocity[0] + self.accel[0] * dt,
                         self.velocity[1] + self.accel[1] * dt)
        self.position = (self.position[0] + self.velocity[0] * dt,
                         self.position[1] + self.velocity[1] * dt)

        # Rotates acording to velocity
        self.rotated_image = pygame.transform.rotate(self.image, vec_angle(self.velocity))

        # Moves the vehicle to the right place
        self.rect.move_ip(self.position)

        # Append debug lines
        self.debug_lines.append(self.velocity)
        self.debug_lines.append(self.accel)

        # Resets acceleration
        self.accel = (0, 0)

    def seek(self, target):
        # Calculates de desired velocity
        desired = vec_sub(target, self.get_center_position())
        distance = vec_mag(desired)
        desired = vec_normalize(desired)

        # Applies arrival behaviour
        if distance < 100:  # TODO: Parameterize min distance
            desired = vec_mult_n(desired, proportional_map(distance, 0, 100, 0, self.maxspeed))
        else:
            desired = vec_mult_n(desired, self.maxspeed)

        # Add desired vector to debug lines
        self.debug_lines.append(desired)

        # Calculates steer accel
        steer = vec_sub(desired, self.velocity)
        steer = vec_limit(steer, 25)

        return steer

    def brake(self):
        # Get nearest obstacles
        self.near_obstacles.clear()
        self.near_obstacles.append(pygame.mouse.get_pos())

        # Creates future path rect
        self.generate_future_path_rect()




        # Pega velocidade e projeta pra alguns segundos
        # Talvez esses segundos tenham a ver com distancia segura
        # Se nesses proximos segundos ele colidir com algo (no caso o mouse)
        #   Faz torricelli pra descobrir aceleração negativa necessário pra frear
        #   Limitar essa aceleracao pelo max brake
        return self

    def apply_force(self, vector):
        self.accel = vec_add(self.accel, vector)

    def draw(self, screen):
        if self.DEBUG:
            # Draws future rect
            screen.blit(self.rotated_future_path, self.position)

        # Draws vehicle on the screen
        screen.blit(self.rotated_image, self.position)

        # Draws debug objects
        if self.DEBUG:
            # Draws debug lines
            # Desired
            pygame.draw.line(pygame.display.get_surface(), (255, 0, 0),  # red
                             self.get_center_position(),
                             vec_add(self.get_center_position(), self.debug_lines[0]), 2)
            # Speed
            pygame.draw.line(pygame.display.get_surface(), (0, 255, 0),  # green
                             self.get_center_position(),
                             vec_add(self.get_center_position(), self.debug_lines[1]), 2)
            # Accel
            pygame.draw.line(pygame.display.get_surface(), (0, 0, 255),  # blue
                             self.get_center_position(),
                             vec_add(self.get_center_position(), self.debug_lines[2]), 2)

        self.debug_lines.clear()

    def get_center_position(self):
        return vec_add(self.position, self.rotated_image.get_rect().center)

    def generate_future_path_rect(self):
        path_distance = 100
        print(self.image.get_size()[1])
        self.future_path = pygame.Surface((path_distance, self.image.get_size()[1]))
        self.future_path.fill((0, 255, 0))
        print(self.velocity)
        self.rotated_future_path = pygame.transform.rotate(self.future_path, vec_angle(self.velocity))

    def get_accel(self):
        return self.accel

    def set_accel(self, accel):
        self.accel = accel

    def get_speed(self):
        return self.velocity

    def set_speed(self, speed):
        self.velocity = speed

    def get_pos(self):
        return self.rect.center[0], self.rect.bottom

    def set_pos(self, pos):
        self.rect.center = (pos[0], pos[1])

    def get_size(self):
        return self.image.get_size()

    @staticmethod
    def metric_to_pixel(n):
        return n / 0.13
