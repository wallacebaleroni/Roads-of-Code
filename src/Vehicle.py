import pygame
from pygame import Vector2

from aux_ops import *


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, vehicle_image, position, velocity=(1, 0), debug=False):
        pygame.sprite.Sprite.__init__(self)

        # Loads image
        self.vehicle_image = vehicle_image
        self.vehicle_image_rotated = self.vehicle_image
        self.vehicle_image_rect = self.vehicle_image.get_rect()

        # Sets debug option and initializes debug lines used to show the vectors acting on the vehicle
        self.DEBUG = debug
        self.debug_lines = []

        # Basic forces
        self.position = Vector2(position)
        self.velocity = Vector2(velocity)
        self.accel = Vector2(0, 0)

        # Get vehicle dimensions
        self.vehicle_length = self.vehicle_image.get_width()
        self.vehicle_width = self.vehicle_image.get_height()

        # Initializes obstacle list
        self.near_obstacles = []

        # Initializes collision buffer
        self.buffer_zone_image = pygame.image.load("../img/buffer_zone.png")
        self.buffer_zone_image_rotated = self.buffer_zone_image
        self.buffer_zone_image_rect = self.buffer_zone_image.get_rect()

    def update(self, dt):
        # Applies seeking behavior
        self.apply_force(self.seek(pygame.mouse.get_pos()))
        self.brake()

        # Updates speed and position
        self.velocity = Vector2(self.velocity[0] + self.accel[0] * dt,
                                self.velocity[1] + self.accel[1] * dt)
        self.position = Vector2(self.position[0] + self.velocity[0] * dt,
                                self.position[1] + self.velocity[1] * dt)

        # Rotates arround center acording to velocity
        pivot = self.vehicle_image_rect.center
        self.vehicle_image_rotated = pygame.transform.rotate(self.vehicle_image, vec_angle(self.velocity))
        self.vehicle_image_rect = self.vehicle_image_rotated.get_rect(center=pivot)

        # Moves the vehicle to the right place
        self.vehicle_image_rect.center = self.position

        # Append debug lines
        self.debug_lines.append(self.velocity)
        self.debug_lines.append(self.accel)

        # Resets acceleration
        self.accel = (0, 0)

    def seek(self, target):
        # Calculates de desired velocity
        desired = vec_sub(target, self.vehicle_image_rect.center)
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

        # Calculates offset
        offset = Vector2(self.vehicle_length / 2, 0) # Starts at the front of the car
        offset += [self.metric_to_pixel(3), 0] # Distance from front of the car

        # Updates buffer zone rotation
        velocity_angle = self.velocity.angle_to((1,0))
        rotated_offset = offset.rotate(-velocity_angle)  # Rotate the offset vector.

        pivot = self.buffer_zone_image_rect.center
        self.buffer_zone_image_rotated = pygame.transform.rotate(self.buffer_zone_image, vec_angle(self.velocity))
        self.buffer_zone_image_rect = self.buffer_zone_image_rotated.get_rect(center=pivot)

        # Updates buffer zone position
        self.buffer_zone_image_rect.center = self.position + rotated_offset

        # Pega velocidade e projeta pra alguns segundos
        # Talvez esses segundos tenham a ver com distancia segura
        # Se nesses proximos segundos ele colidir com algo (no caso o mouse)
        #   Faz torricelli pra descobrir aceleração negativa necessário pra frear
        #   Limitar essa aceleracao pelo max brake
        return self

    def apply_force(self, vector):
        self.accel = vec_add(self.accel, vector)

    def draw(self, screen):
        # Draws vehicle on the screen
        screen.blit(self.vehicle_image_rotated, self.vehicle_image_rect)

        # Draws more debug objects
        if self.DEBUG:
            # Draws debug lines
            # Desired
            pygame.draw.line(pygame.display.get_surface(), (255, 0, 0),  # red
                             self.vehicle_image_rect.center,
                             vec_add(self.vehicle_image_rect.center, self.debug_lines[0]), 2)
            # Speed
            pygame.draw.line(pygame.display.get_surface(), (0, 255, 0),  # green
                             self.vehicle_image_rect.center,
                             vec_add(self.vehicle_image_rect.center, self.debug_lines[1]), 2)
            # Accel
            pygame.draw.line(pygame.display.get_surface(), (0, 0, 255),  # blue
                             self.vehicle_image_rect.center,
                             vec_add(self.vehicle_image_rect.center, self.debug_lines[2]), 2)

            # Draws rotation indicators
            pygame.draw.circle(pygame.display.get_surface(), (255, 250, 70), self.vehicle_image_rect.center, 3)
            pygame.draw.rect(pygame.display.get_surface(), (30, 250, 70), self.vehicle_image_rect, 1)

        self.debug_lines.clear()

    def get_accel(self):
        return self.accel

    def set_accel(self, accel):
        self.accel = accel

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, speed):
        self.velocity = speed

    def get_pos(self):
        return self.vehicle_image_rect.center[0], self.vehicle_image_rect.bottom

    def set_pos(self, pos):
        self.vehicle_image_rect.center = (pos[0], pos[1])

    def get_size(self):
        return self.vehicle_image.get_size()

    @staticmethod
    def metric_to_pixel(n):
        return n / 0.13
