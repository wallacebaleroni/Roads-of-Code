import pygame
from pygame import Vector2
import math

from metrics import *
from GameObject import *


class Vehicle(GameObject):
    def __init__(self, image, position=Vector2(0, 0), velocity=Vector2(1, 0), debug=False):
        GameObject.__init__(self, image, position)

        # Loads image (image and image_rect created on super class)
        self.image_rotated = self.image

        # Sets debug option and initializes debug lines used to show the vectors acting on the vehicle
        self.DEBUG = debug
        pygame.font.init()
        self.textFont = pygame.font.SysFont('Arial', 15)
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

        # Initializes collision variables
        self.safe_distance = metric_to_pixel(3)
        self.collision_imminent = True
        self.braking = None

    def update(self, dt=0, neighbourhood={}):
        # Selects mouse and applies seeking behavior
        self.apply_accel(self.seek(neighbourhood["mouse"].get_pos()))
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
            desired = desired * proportional_map(distance, 0, 100, 0, self.max_velocity)
        else:
            desired = desired * self.max_velocity

        # Add desired vector to debug lines
        self.debug_lines.append(desired)

        # Calculates steer accel
        steer = desired - self.velocity
        steer.scale_to_length(pixel_to_metric(self.max_acceleration))

        # TODO: As the steering is, in the end, what controls the braking, it's not possible to...
        # TODO: ...limit it without detaching the breaking from the steering
        steer_angle = steer.angle_to(self.velocity)
        if abs(steer_angle) > abs(self.max_steer_angle):
            if steer_angle < 0:
                steer[0] = steer[1] / math.tan(math.radians(-self.max_steer_angle))
            else:
                steer[0] = steer[1] / math.tan(math.radians(self.max_steer_angle))

        return steer

    def brake(self, neighbourhood):
        self.update_buffer_zone()

        # Checks collision and calculates distance from the closest neighbour
        dist = 0
        if self.buffer_zone_image_rect.colliderect(neighbourhood["mouse"].image_rect):
            self.collision_imminent = True
            dist = self.get_pos() - neighbourhood["mouse"].get_pos()
        else:
            self.collision_imminent = False
            self.braking = None

        # If there's an imminent collision and the braking is not yet calculated
        if self.collision_imminent and self.braking is None:
            # Calculates braking
            scalar_dist = dist.length()
            scalar_dist -= self.safe_distance
            braking_mag = (-self.get_velocity().length_squared()) / (2 * scalar_dist)

            # Limits breaking
            if abs(braking_mag) > abs(self.max_brake):
                if braking_mag < 0:
                    braking_mag = -self.max_brake
                else:
                    braking_mag = self.max_brake

            # Rotates vector to be parallel to the velocity
            self.braking = Vector2(abs(braking_mag), 0)
            self.braking.rotate_ip(self.braking.angle_to(self.velocity))
            self.braking.rotate_ip(180)

        if self.braking is not None:
            self.accel = self.braking

    def update_buffer_zone(self):
        # Calculates safe distance
        safe_distance = self.safe_distance + (self.velocity.length() / metric_to_pixel(5.5)) * self.vehicle_length
        if safe_distance < 1:
            safe_distance = 1

        # Calculates rotated offset
        offset = Vector2(self.vehicle_length / 2, 0)  # Starts at the front of the car
        offset += Vector2(safe_distance, 0) / 2  # Distance from front of the car
        self.buffer_zone_image = pygame.transform.scale(self.buffer_zone_image,
                                                        (int(safe_distance), self.buffer_zone_image.get_height()))

        # Updates buffer zone rotation
        velocity_angle = self.velocity.angle_to((1, 0))
        rotated_offset = offset.rotate(-velocity_angle)  # Rotate the offset vector.

        pivot = self.buffer_zone_image_rect.center
        self.buffer_zone_image_rotated = pygame.transform.rotate(self.buffer_zone_image, self.velocity.angle_to((1, 0)))
        self.buffer_zone_image_rect = self.buffer_zone_image_rotated.get_rect(center=pivot)

        # Updates buffer zone position
        self.buffer_zone_image_rect.center = self.position + rotated_offset

    def apply_accel(self, vector):
        self.accel = self.accel + Vector2(vector)

    def draw(self, screen):
        # Draws debug objects
        if self.DEBUG:
            # Selects color of buffer zone
            self.buffer_zone_image = self.buffer_zone_red if self.collision_imminent else self.buffer_zone_green
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

            # Draws metrics
            velocity_text = self.textFont.render("Velocity: %0.2f km/h" % (pixel_to_metric(Vector2(self.get_velocity()).length()) * 3.6), False, (255, 255, 255))
            accel_text = self.textFont.render("Accel: %0.2f km/h" % (pixel_to_metric(Vector2(self.get_accel()).length()) * 3.6), False, (255, 255, 255))

            screen.blit(velocity_text, Vector2(screen.get_size()) - Vector2(velocity_text.get_size()))
            screen.blit(accel_text, Vector2(screen.get_size()) - Vector2((accel_text.get_width(), 2 * accel_text.get_height())))

        self.debug_lines.clear()

    def toggle_debug(self):
        self.DEBUG = not self.DEBUG

    def get_accel(self):
        return self.debug_accel

    def set_accel(self, accel):
        self.accel = accel

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, speed):
        self.velocity = speed

    def get_pos(self):
        # Returns the position of the front of the vehicle
        front_distance = self.image.get_width() / 2
        relative_vehicle_front = Vector2(front_distance, 0).rotate(Vector2(1,0).angle_to(self.velocity))

        return self.image_rect.center + relative_vehicle_front

    def get_size(self):
        return self.image.get_size()
