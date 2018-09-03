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

    def update(self, dt):
        # Applies seeking behavior
        self.apply_force(self.seek(pygame.mouse.get_pos()))

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
        desired = vec_sub(target, self.position)
        desired = vec_set_mag(desired, self.maxspeed)

        # Add desired vector to debug lines
        self.debug_lines.append(desired)

        # Calculates steer accel
        steer = vec_sub(desired, self.velocity)
        steer = vec_limit(steer, 25)

        return steer

    def apply_force(self, vector):
        self.accel = vec_add(self.accel, vector)

    def draw(self, screen):
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
