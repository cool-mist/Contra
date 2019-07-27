import pygame
from utils import Colors


class Ground(pygame.sprite.Sprite):
    """Platform"""

    def __init__(self, x, y, w, h, camera):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(Colors.YELLOW)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.defaultx = x
        self.defaulty = y
        self.camera = camera

    def update(self):
        self.rect.x = self.defaultx + self.camera.pos.x
        self.rect.y = self.defaulty + self.camera.pos.y


class Background(pygame.sprite.Sprite):
    """Background"""

    def __init__(self, bg, camera):
        pygame.sprite.Sprite.__init__(self)
        self.image = bg
        self.rect = self.image.get_rect()
        self.camera = camera
        self.rect.left = camera.pos.x
        self.rect.y = camera.pos.y

    def update(self):
        self.rect.x = self.camera.pos.x
        self.rect.y = self.camera.pos.y


class HUD(pygame.sprite.Sprite):
    def __init__(self, max_player_health, max_blink_retract, width):
        pygame.sprite.Sprite.__init__(self)
        pygame.font.init()
        self.surface = pygame.Surface((width, 40))
        self.surface.fill(Colors.WHITE)
        self.image = self.surface
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 0
        self.width = width
        self.font = pygame.font.SysFont("monospace", 20)
        self.max_player_health = max_player_health
        self.max_blink_retract = max_blink_retract

    # Health indicator
    # Bullets indicator
    # Powerup indicator
    # Blink Indicator
    def update(self):
        pass

    def update_HUD(self, game):
        self.surface = pygame.Surface((self.width, 30))
        self.surface.fill(Colors.LIGHT_YELLOW)
        self.drawHealth(game.health)
        self.drawBlink(game.blinkRetract)
        self.drawPowerup()
        pass

    def drawHealth(self, health):
        if health > self.max_player_health - 5:
            text = self.font.render(
                "Health: "+str(health), 1, Colors.DARK_GREEN)
        elif health > 10:
            text = self.font.render(
                "Health: "+str(health), 1, Colors.DARK_YELLOW)
        else:
            text = self.font.render("Health: "+str(health), 1, Colors.RED)
        textPos = text.get_rect()
        textPos.centerx = 130
        self.surface.blit(text, textPos)
        self.image = self.surface

    def drawBlink(self, retract):
        retractPerc = str(100 - int(retract/self.max_blink_retract*100))
        if retractPerc == '100':
            retractPerc = "ONLINE"
            text = self.font.render("Dash: "+retractPerc, 1, Colors.DARK_GREEN)
        else:
            text = self.font.render("Dash: "+retractPerc, 1, Colors.RED)
        textPos = text.get_rect()
        textPos.centerx = 410
        self.surface.blit(text, textPos)
        self.image = self.surface

    def drawPowerup(self):
        pass


class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, ptype, image, speed, camera):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        # if ptype == 1:
        #     self.image = POWERUP_BULLET
        # elif ptype == 0:
        #     self.image = POWERUP_BLINK
        # else:
        #     self.image = POWERUP_SLOW
        self.rect = self.image.get_rect()
        self.image.set_colorkey(Colors.BLACK)
        if x > 6164:
            x = 6160
        self.rect.x = x
        self.defaultx = x
        self.rect.y = -5
        self.speed = speed
        self.camera = camera

        self.ptype = ptype

    def update(self):
        if not self.rect.y >= 170:
            self.rect.y += self.speed

        self.rect.x = self.camera.pos.x + self.defaultx
        if self.rect.x < 0:
            self.kill()

    def powerup(self):
        # perform the action of the powerup
        return self.ptype
        pass
