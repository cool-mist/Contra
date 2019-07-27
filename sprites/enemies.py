"""Enemy sprites"""
import pygame
from states import States
from utils import Colors
from bullet import Bullet
Vec = pygame.math.Vector2


class Sniper(pygame.sprite.Sprite):
    """Stationary sniper, tries to shoot at the player sprite"""

    def __init__(self, x, y, sniper_range, image, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((player.width, player.height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.up = False
        self.down = False
        self.speedy = 0
        self.defaultx = x
        self.defaulty = y
        self.counter = 60
        self.state = States.LEFT
        self.image = image
        self.player = player
        self.sniper_range = sniper_range

    def scale_image(self, image):
        return pygame.transform.scale(image,
                                      (self.player.width, self.player.height))

    def update(self):
        # Update sprite image based on state
        if self.state == States.LEFT:
            self.image = self.scale_image(self.image.left)
        elif self.state == States.LEFT_UP:
            self.image = self.scale_image(self.image.left_up)
        else:
            self.image = self.scale_image(self.image.left_down)

        self.image.set_colorkey(Colors.YELLOW)
        self.rect.x = self.defaultx + self.camera.pos.x
        self.rect.y = self.defaulty + self.camera.pos.y

        # if self.state == States.LEFT:
        #     self.image = pygame.transform.scale(
        #         SNIPER_LEFT, (PLAYER_WIDTH, PLAYER_HEIGHT))
        # elif self.state == LEFT_UP:
        #     self.image = pygame.transform.scale(
        #         SNIPER_LEFT_UP, (PLAYER_WIDTH, PLAYER_HEIGHT))
        # else:
        #     self.image = pygame.transform.scale(
        #         SNIPER_LEFT_DOWN, (PLAYER_WIDTH, PLAYER_HEIGHT))
        # self.image.set_colorkey(YELLOW)
        # self.rect.x = self.defaultx + CAMERA.pos.x
        # self.rect.y = self.defaulty + CAMERA.pos.y
        pass

    def shoot_towards(self, player):
        # print(str(player.rect.bottom)+","+str(self.rect.bottom))
        if player.rect.top < self.rect.top:
            self.down = True
            self.up = False
            self.state = States.LEFT_DOWN
        elif player.rect.center[1] > self.rect.bottom:
            self.up = True
            self.down = False
            self.state = States.LEFT_UP
        else:
            self.up, self.down = False, False
            self.state = States.LEFT
        if (self.rect.x < player.pos.x + self.sniper_range
                and self.rect.x > player.pos.x):
            if self.counter == 0:
                self.counter = 60
                return self.shoot(self.up, self.down)
            else:
                self.counter -= 1
                return None

    def shoot(self, up, down):
        sx = -1
        if up:
            sy = 1
        elif down:
            sy = -1
        else:
            sy = 0
        b = Bullet(self.rect.left, self.rect.bottom, sx, sy)
        return b


class Soldier(pygame.sprite.Sprite):
    """Soldier that runs towards the player"""

    def __init__(self, x, y, speed, acc, frames, player, camera, fps):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            frames[0], (player.width, player.height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = Vec(x, y)
        self.vel = Vec(-speed.vx, 0)
        self.acc = Vec(0, acc)
        self.player = player
        self.camera = camera

        # Animation
        self.soldier_frames = frames
        self.animIndex = 0
        self.animCounter = fps

    def animate(self):
        self.animCounter -= 1
        if self.animCounter == 0:
            self.animIndex += 1
            self.animIndex %= len(self.soldier_frames)
            self.image = pygame.transform.scale(
                self.soldier_frames[self.animIndex],
                (self.player.width, self.player.height))
            self.animCounter = self.animCounter
        self.image.set_colorkey(Colors.YELLOW)

    def update(self):
        if self.rect.right < 0:
            self.kill()
        self.animate()
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
        self.rect.x = self.pos.x + self.camera.pos.x
        self.rect.bottom = self.pos.y + self.camera.pos.y

    def shoot_towards(self, player):
        # Shoot towards the player.
        pass


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, image, player, camera):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = Vec(x, y)
        self.counter = 60
        self.camera = camera

    def update(self):
        self.rect.x = self.pos.x + self.camera.pos.x
        self.counter -= 1
        pass

    def shoot(self):
        if self.rect.x > self.player.pos.x:
            if self.counter == 0 or self.counter == 5:
                if self.counter == 0:
                    self.counter = 60
                return Bullet(self.rect.x, self.rect.bottom, -1, 0)
        return None
