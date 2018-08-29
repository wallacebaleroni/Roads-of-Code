from src.GameObject import *
from src.vector_ops import *


class Vehicle(GameObject):
    def __init__(self, image, position, velocity=(1, 0)):
        GameObject.__init__(self, image, position, velocity)

        self.maxspeed = self.metric_to_pixel(22)
        self.maxaccel = self.metric_to_pixel(10)

    def update(self, dt):
        seek_accel = self.seek(pygame.mouse.get_pos())
        self.accel = seek_accel

        GameObject.update(self, dt)

    def seek(self, target):
        desired = vec_sub(target, self.position)
        desired = vec_set_mag(desired, self.maxspeed)

        steer = vec_sub(desired, self.speed)
        steer = vec_limit(steer, 100)

        return steer

    @staticmethod
    def metric_to_pixel(n):
        return n / 0.13