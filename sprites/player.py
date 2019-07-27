import pygame
from utils import Colors
from states import States
from bullet import Bullet
Vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    """Player controlled sprite"""

    def __init__(self, game, x, y, accy, initial, width, height, right_frames,
                 right_up_frames, right_down_frames, dead_frames, jump_frames,
                 health, blink_time, blink_retract, blink_speed, dash_sound,
                 shoot_sound, bullet_threshold, camera, friction, jump_height,
                 fps):
        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.image = pygame.transform.scale(initial, (width, height))
        self.image.set_colorkey(Colors.YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, 0)
        self.health = health
        self.max_health = health
        self.height = height
        self.width = width

        # Camera
        self.camera = camera
        self.bullet_threshold = bullet_threshold

        # Movement
        self.pos = {x: x, y: y}
        self.state = States.RIGHT
        self.up = False
        self.down = False
        self.pos = Vec(30, 30)
        self.vel = Vec(0, 0)
        self.acc = Vec(0, accy)
        self.canMove = True
        self.jumping = True
        self.facing = 1
        self.friction = friction

        # Jumping
        self.can_jump = False
        self.collisions = True
        self.jump_height = jump_height

        # Blinking
        self.blink_time = blink_time
        self.canBlink = 1
        self.blinking = False
        self.blink_retract = blink_retract
        self.max_blink_retract = blink_retract
        self.blink_time = blink_time
        self.max_blink_time = blink_time

        self.dead = False
        # Animation
        # Frames hold each frame
        # index determines the current frame to be played
        self.animCounter = fps

        self.jumpFrames = jump_frames
        self.jumpIndex = 0

        self.rightFrames = right_frames
        self.rightIndex = 0

        self.rightUpFrames = right_up_frames
        self.rightUpIndex = 0

        self.rightDownFrames = right_down_frames
        self.rightDownIndex = 0

        self.deadFrames = dead_frames
        self.deadIndex = 0

        # Sounds
        self.shoot_sound = shoot_sound
        self.dash_sound = dash_sound

    def update(self):
        self.calcState()
        if self.dead:
            self.kill()
            return
        if self.jumping:
            self.jumpIndex = self.animate(
                self.jumpFrames, self.jumpIndex,
                int(self.height/2), self.width)

        else:
            self.setImageByState()
            if self.isMoving():
                # Set the animation depending on the state
                if self.state == States.RIGHT:
                    self.rightIndex = self.animate(
                        self.rightFrames, self.rightIndex,
                        self.width, self.height)

                elif self.state == States.RIGHT_DOWN:
                    self.rightDownIndex = self.animate(
                        self.rightDownFrames, self.rightDownIndex,
                        self.width, self.height)

                elif self.state == States.RIGHT_UP:
                    self.rightUpIndex = self.animate(
                        self.rightUpFrames, self.rightUpIndex,
                        self.width, self.height)

                elif self.state == States.LEFT:
                    self.rightIndex = self.animate(
                        self.rightFrames, self.rightIndex,
                        self.width, self.height, True)

                elif self.state == States.LEFT_DOWN:
                    self.rightDownIndex = self.animate(
                        self.rightDownFrames, self.rightDownIndex,
                        self.width, self.height, True)

                elif self.state == States.LEFT_UP:
                    self.rightUpIndex = self.animate(
                        self.rightUpFrames, self.rightUpIndex,
                        self.width, self.height, True)
            else:
                # Else a stationary image
                if self.state == States.RIGHT:
                    self.image = pygame.transform.scale(
                        self.right_frames[0], (self.width, self.height))
                elif self.state == States.RIGHT_DOWN:
                    self.image = pygame.transform.scale(
                        self.right_down_frames[0], (self.width, self.height))
                elif self.state == States.RIGHT_UP:
                    self.image = pygame.transform.scale(
                        self.right_up_frames[0], (self.width, self.height))
                elif self.state == States.LEFT:
                    self.image = pygame.transform.flip(pygame.transform.scale(
                        self.right_frames[0], (self.width, self.height)),
                        True, False)
                elif self.state == States.LEFT_DOWN:
                    self.image = pygame.transform.flip(pygame.transform.scale(
                        self.right_down_frames[0], (self.width, self.height)),
                        True, False)
                elif self.state == States.LEFT_UP:
                    self.image = pygame.transform.flip(pygame.transform.scale(
                        self.right_up_frames[0], (self.width, self.height)),
                        True, False)

        # Blinking and Motion are Disjoint. All others can occur simultaneously
        if self.blinking:
            self.acc = Vec(0, 0)
            self.vel.y = 0
            self.vel.x = self.facing * self.blink_speed
            self.blink_time -= 1
            self.blink_retract -= 1
            if self.blink_time == 0:
                self.blinking = False
                self.blink_time = self.max_blink_time
                self.blink_retract = self.max_blink_retract
        else:
            self.acc = Vec(0, self.accy)
            if self.blink_retract == 0:
                pass
            else:
                self.blink_retract -= 1
        keystate = pygame.key.get_pressed()
        mousestate = pygame.mouse.get_pressed()
        if keystate[pygame.K_s]:
            self.acc.x = -self.accy
            self.facing = -1
        if keystate[pygame.K_d]:
            self.acc.x = self.accy
            self.facing = 1
        if keystate[pygame.K_x]:
            self.acc = Vec(0, self.accy)
            self.vel = Vec(0, 0)
        if keystate[pygame.K_s]:
            self.drop()
        if mousestate[2]:   # RMB
            if self.canBlink:
                self.blink()
        if (not self.pos.x < -self.camera.left_bound and not self.pos.x >
                -self.camera.right_bound):

            self.acc.x += self.vel.x * self.friction
            self.vel += self.acc
            self.pos += self.vel + 0.5*self.acc
        else:
            if self.pos.x <= -self.camera.left_bound:
                self.pos.x += 1
            else:
                self.pos.x -= 1
        self.rect.bottom = self.pos.y
        self.image.set_colorkey(Colors.YELLOW)

    def isMoving(self):
        if int(self.vel.x):
            return True
        return False

    def jump(self):

        if self.canMove and self.can_jump and self.vel.y == 0:
            self.vel.y = -self.jump_height
            self.jumping = True
            self.can_jump = False

    def blink(self):
        if self.canMove and self.blink_retract == 0:
            self.blink_retract = self.max_blink_retract
            self.dash_sound.play()
            self.blinking = True

    def stopJumping(self):
        self.jumpIndex = 0
        self.jumping = False

    def animate(self, frames, index, width, height, flip=False):
        self.animCounter -= 1
        if self.animCounter == 0:
            index += 1
            # print(index)
            index %= len(frames)
            if not flip:
                self.image = pygame.transform.scale(
                    frames[index], (width, height))
            else:
                self.image = pygame.transform.flip(pygame.transform.scale(
                    frames[index], (width, height)), True, False)
            self.animCounter = self.fps
        rx = self.rect.left
        ry = self.rect.top
        self.rect = self.image.get_rect()
        self.rect.left = rx
        self.rect.top = ry
        return index

    def drop(self):
        if self.canMove:
            self.collisions = False

    def shoot(self, mousePos):
        self.calcState()
        if self.state == States.RIGHT:
            speedx, speedy = 1, 0
            pass
        elif self.state == States.LEFT:
            speedx, speedy = -1, 0
            pass
        elif self.state == States.RIGHT_UP:
            speedx, speedy = 1, 1
            pass
        elif self.state == States.RIGHT_DOWN:
            speedx, speedy = 1, -1
            pass
        elif self.state == States.LEFT_UP:
            speedx, speedy = -1, 1
            pass
        elif self.state == States.LEFT_DOWN:
            speedx, speedy = -1, -1
            pass
        self.shoot_sound.play()
        b = Bullet(self.pos.x, self.pos.y, speedx, speedy)
        return b

    def calcState(self):
        mouseX, mouseY = pygame.mouse.get_pos()

        if mouseY > self.pos.y + self.bullet_threshold:
            self.up = True
            self.down = False
        elif mouseY < self.pos.y - self.bullet_threshold:
            self.up = False
            self.down = True
        else:
            self.up = False
            self.down = False

        if self.facing == 1:
            if self.up:
                self.state = States.RIGHT_UP
            elif self.down:
                self.state = States.RIGHT_DOWN
            else:
                self.state = States.RIGHT
        else:
            if self.up:
                self.state = States.LEFT_UP
            elif self.down:
                self.state = States.LEFT_DOWN
            else:
                self.state = States.LEFT

    def setImageByState(self):
        if self.state == States.RIGHT and not self.isMoving():
            self.image = pygame.transform.scale(
                self.initial, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.left = self.player.pos.x

    def die(self):
        print("DEAD")
        self.dead = True
        self.health = self.max_health
