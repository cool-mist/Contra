"""The Bullet Sprite"""
import pygame
from utils import Colors


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, speed, image, kill_width):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.image.set_colorkey(Colors.WHITE)
        self.rect.left = pos.x
        self.rect.top = pos.y-50
        self.speed = speed
        self.kill_width = kill_width

    def update(self):
        self.rect.left += self.speed.vx
        self.rect.top += self.speed.vy

        if self.rect.right < 0 or self.rect.left > self.kill_width:
            self.kill()
