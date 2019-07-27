"""Set of utility functions"""
import os
import pygame
import enum


class Colors(enum.Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    DARK_GREEN = (2, 207, 16)
    BLUE = (0, 0, 255)
    SEA_BLUE = (0, 86, 255)
    LIGHT_YELLOW = (255, 251, 168)
    YELLOW = (255, 255, 0)
    DARK_YELLOW = (255, 150, 2)


class GameResources():
    """Fetch resources/assets used in the game"""

    def __init__(self, base_dir):
        self.base_dir = base_dir

    def get_resource(self, path):
        """Fetch relative path to the base directory"""
        return GameResources(self.get_path(path))

    def get_path(self, path):
        """Fetch the file in this directory"""
        return os.path.join(self.base_dir, path)

    def load_image(self, path):
        """Loads pygame image at this relative path"""
        return pygame.image.load(self.get_path(path)).convert()

    def load_spritesheet(self, path):
        """Loads a spritesheet at this relative path"""
        return SpriteSheet(self.get_path(path))

    def load_sound(self, path):
        """Loads the sound"""
        return pygame.mixer.Sound(self.get_path(path))


class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pygame.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assuming black works as the transparent color
        image.set_colorkey(Colors.BLACK)

        # Return the image
        return image


class Speed():
    def __init__(self, x, y, mag):
        self.x = x
        self.y = y
        self.mag = mag
        self.vx = mag * x
        self.vy = mag * y


class Pos():
    def __init__(self, x, y):
        self.x = x
        self.y = y

