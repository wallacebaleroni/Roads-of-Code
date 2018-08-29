import pygame


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, position, speed=(1, 0)):
        pygame.sprite.Sprite.__init__(self)

        self.image = image

        self.rect = self.image.get_rect()
        self.area = pygame.display.get_surface().get_rect()

        self.position = position
        self.speed = speed
        self.accel = (0, 0)

    def update(self, dt):
        self.speed = (self.speed[0] + self.accel[0] * dt,
                      self.speed[1] + self.accel[1] * dt)
        self.position = (self.position[0] + self.speed[0] * dt,
                         self.position[1] + self.speed[1] * dt)

        self.rect.move_ip(self.position)

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def get_accel(self):
        return self.accel

    def set_accel(self, accel):
        self.accel = accel

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def get_pos(self):
        return self.rect.center[0], self.rect.bottom

    def set_pos(self, pos):
        self.rect.center = (pos[0], pos[1])

    def get_size(self):
        return self.image.get_size()
