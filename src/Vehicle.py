import pygame
from pygame import Vector2

from src.metrics import *
from src.GameObject import GameObject


class Vehicle(GameObject):
    def __init__(self, image, position=Vector2(0, 0), velocity=Vector2(1, 0), debug=False):
        GameObject.__init__(self, image, position)

        # Loads image (image and image_rect created on super class)
        self.image_rotated = self.image

        # Sets debug option and initializes debug lines used to show the vectors acting on the vehicle
        self.DEBUG = debug
        self.debug_lines = []

        # Basic forces (position created on super class)
        self.velocity = Vector2(velocity)
        self.accel = Vector2(0, 0)
        self.debug_accel = self.accel

        # Get vehicle dimensions
        self.vehicle_length = self.image.get_width()
        self.vehicle_width = self.image.get_height()

        # Initializes collision buffer
        self.buffer_zone_green = pygame.image.load("../img/buffer_zone_green.png")
        self.buffer_zone_red = pygame.image.load("../img/buffer_zone_red.png")
        self.buffer_zone_image = self.buffer_zone_green
        self.buffer_zone_image_rotated = self.buffer_zone_image
        self.buffer_zone_image_rect = self.buffer_zone_image.get_rect()

    def update(self, dt=0, neighbourhood={}):
        # Selects mouse and applies seeking behavior
        self.apply_force(self.seek(neighbourhood["mouse"].get_pos()))
        self.brake(neighbourhood)

        # Updates speed and position
        self.velocity = Vector2(self.velocity[0] + self.accel[0] * dt,
                                self.velocity[1] + self.accel[1] * dt)
        self.position = Vector2(self.position[0] + self.velocity[0] * dt,
                                self.position[1] + self.velocity[1] * dt)

        # Rotates around center according to velocity
        pivot = self.image_rect.center
        self.image_rotated = pygame.transform.rotate(self.image, self.velocity.angle_to((1, 0)))
        self.image_rect = self.image_rotated.get_rect(center=pivot)

        # Moves the vehicle to the right place
        self.image_rect.center = self.position

        # Append debug lines
        self.debug_lines.append(self.velocity)
        self.debug_lines.append(self.accel)

        # Saves and resets acceleration
        self.debug_accel = self.accel
        self.accel = Vector2(0, 0)

    def seek(self, target):
        # Calculates de desired velocity
        desired = target - self.image_rect.center
        distance = desired.length()
        if desired != (0, 0):
            desired = desired.normalize()

        # Applies arrival behaviour
        if distance < 100:  # TODO: Parameterize min distance
            desired = desired * proportional_map(distance, 0, 100, 0, self.maxspeed)
        else:
            desired = desired * self.maxspeed

        # Add desired vector to debug lines
        self.debug_lines.append(desired)

        # Calculates steer accel
        steer = desired - self.velocity
        steer.scale_to_length(25)

        return steer

    def brake(self, neighbourhood):
        # Checks collision with neighbourhood
        if self.buffer_zone_image_rect.colliderect(neighbourhood["mouse"].image_rect):
            self.buffer_zone_image = self.buffer_zone_red
        else:
            self.buffer_zone_image = self.buffer_zone_green

        # Calculates offset
        offset = Vector2(self.vehicle_length / 2, 0) # Starts at the front of the car
        offset += [(self.velocity.length() / metric_to_pixel(5.5)) * self.vehicle_length, 0] # Distance from front of the car

        # Updates buffer zone rotation
        velocity_angle = self.velocity.angle_to((1,0))
        rotated_offset = offset.rotate(-velocity_angle)  # Rotate the offset vector.

        pivot = self.buffer_zone_image_rect.center
        self.buffer_zone_image_rotated = pygame.transform.rotate(self.buffer_zone_image, self.velocity.angle_to((1,0)))
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
        self.accel = self.accel + Vector2(vector)

    def draw(self, screen):
        # Draws debug objects
        if self.DEBUG:
            # Draws buffer zone
            screen.blit(self.buffer_zone_image_rotated, self.buffer_zone_image_rect)

        # Draws vehicle on the screen
        screen.blit(self.image_rotated, self.image_rect)

        # Draws more debug objects
        if self.DEBUG:
            # Draws debug lines
            # Desired
            pygame.draw.line(pygame.display.get_surface(), (255, 0, 0),  # red
                             self.image_rect.center,
                             self.image_rect.center + self.debug_lines[0], 2)
            # Speed
            pygame.draw.line(pygame.display.get_surface(), (0, 255, 0),  # green
                             self.image_rect.center,
                             self.image_rect.center + self.debug_lines[1], 2)
            # Accel
            pygame.draw.line(pygame.display.get_surface(), (0, 0, 255),  # blue
                             self.image_rect.center,
                             self.image_rect.center + self.debug_lines[2], 2)

            # Draws rotation indicators
            pygame.draw.circle(pygame.display.get_surface(), (255, 250, 70), self.image_rect.center, 3)
            pygame.draw.rect(pygame.display.get_surface(), (30, 250, 70), self.image_rect, 1)

        self.debug_lines.clear()

    def get_accel(self):
        return self.debug_accel

    def set_accel(self, accel):
        self.accel = accel

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, speed):
        self.velocity = speed

    def get_pos(self):
        return Vector2(self.image_rect.center[0], self.image_rect.bottom)

    def get_size(self):
        return self.image.get_size()
