import pygame
from pygame import Vector2


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, position=Vector2(0,0)):
        pygame.sprite.Sprite.__init__(self)

        # Sets initial position
        self.position = position

        # Initializes image
        self.image = image
        self.image_rect = self.image.get_rect()

    def update(self, dt=0, neighbourhood={}):
        self.image_rect.center = self.position

    def draw(self, screen):
        screen.blit(self.image, self.image_rect)

    def set_pos(self, pos):
        self.position = Vector2(pos)

    def get_pos(self):
        return self.position