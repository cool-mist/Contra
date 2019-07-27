"""Effects/animations that do not interact otherwise"""
import pygame
from utils import Colors


class Death(pygame.sprite.Sprite):
    """Kill animation"""

    def __init__(self, x, y, frames, sound):
        pygame.sprite.Sprite.__init__(self)
        self.image = frames[0]
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.defaultx = x
        self.rect.top = y
        self.time = 0
        self.image.set_colorkey(Colors.WHITE)
        self.explosionFrames = frames

        sound.play()

    def update(self):
        self.time += 1
        if self.time == 5:
            self.kill()
            return
        self.image = self.explosionFrames[self.time]
        self.image.set_colorkey(Colors.WHITE)

        pass
