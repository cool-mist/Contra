"""Defines the camera of the game"""
import pygame
Vec = pygame.math.Vector2


class Camera(object):
    """Camera centered at the player."""

    def __init__(self, left_bound, right_bound):
        self.pos = Vec(0, 0)
        self.left_bound = left_bound
        self.right_bound = right_bound

    def update(self, sprite):
        if sprite.canMove:
            self.pos.x = -sprite.pos.x
        if self.pos.x >= self.left_bound:
            self.pos.x = self.left_bound
        elif self.pos.x <= self.right_bound:
            self.pos.x = self.right_bound
