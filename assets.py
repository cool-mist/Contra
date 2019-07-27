"""Loads all the assets used in the game"""
import pygame
from settings import IMG_FOLDER, SOUND_FOLDER, WINDOW_SIZE

# Load graphics
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

SCREEN = pygame.display.set_mode(WINDOW_SIZE)

# Start Screen Background
START_SCREEN_BACKGROUND = IMG_FOLDER.load_image('start.jpg')

# Background image
LEVEL1_BACKGROUND = IMG_FOLDER.load_image('l1.png')

# Bullet images
BULLET_IMAGE = IMG_FOLDER.load_image('bullet.png')

# Mob images
SOLDIER_SHEET = IMG_FOLDER.load_spritesheet('enemies.png')

# Player Images
PLAYER_SHEET = IMG_FOLDER.load_spritesheet('playersheet.png')

PLAYER_RIGHT_0 = PLAYER_SHEET.get_image(145, 15, 25, 37).convert()
PLAYER_RIGHT_1 = PLAYER_SHEET.get_image(144, 133, 22, 36).convert()
PLAYER_RIGHT_2 = PLAYER_SHEET.get_image(167, 134, 22, 36).convert()
PLAYER_RIGHT_3 = PLAYER_RIGHT_0
PLAYER_RIGHT_4 = PLAYER_SHEET.get_image(190, 135, 24, 35).convert()
PLAYER_RIGHT_5 = PLAYER_SHEET.get_image(218, 133, 19, 35).convert()
PLAYER_RIGHT_6 = PLAYER_SHEET.get_image(242, 132, 18, 37).convert()

PLAYER_RIGHT_UP_0 = PLAYER_SHEET.get_image(145, 95, 20, 35).convert()
PLAYER_RIGHT_UP_1 = PLAYER_SHEET.get_image(171, 95, 23, 33).convert()
PLAYER_RIGHT_UP_2 = PLAYER_SHEET.get_image(199, 96, 25, 34).convert()

PLAYER_RIGHT_DOWN_0 = PLAYER_SHEET.get_image(144, 55, 19, 36).convert()
PLAYER_RIGHT_DOWN_1 = PLAYER_SHEET.get_image(170, 56, 19, 35).convert()
PLAYER_RIGHT_DOWN_2 = PLAYER_SHEET.get_image(195, 56, 23, 35).convert()

PLAYER_JUMP_0 = PLAYER_SHEET.get_image(183, 176, 22, 17).convert()
PLAYER_JUMP_1 = PLAYER_SHEET.get_image(206, 171, 17, 20).convert()
PLAYER_JUMP_2 = PLAYER_SHEET.get_image(225, 175, 22, 17).convert()
PLAYER_JUMP_3 = PLAYER_SHEET.get_image(249, 172, 17, 20).convert()

PLAYER_DEAD_0 = PLAYER_SHEET.get_image(144, 198, 25, 19).convert()
PLAYER_DEAD_1 = PLAYER_SHEET.get_image(170, 193, 19, 23).convert()
PLAYER_DEAD_2 = PLAYER_SHEET.get_image(192, 198, 22, 18).convert()
PLAYER_DEAD_3 = PLAYER_SHEET.get_image(219, 194, 17, 22).convert()
PLAYER_DEAD_4 = PLAYER_SHEET.get_image(238, 204, 35, 11).convert()

# Sniper
SNIPER_SHEET = IMG_FOLDER.load_spritesheet('enemies.png')

SNIPER_LEFT_DOWN = SNIPER_SHEET.get_image(135, 249, 32, 57).convert()
SNIPER_LEFT = SNIPER_SHEET.get_image(98, 261, 37, 47).convert()
SNIPER_LEFT_UP = SNIPER_SHEET.get_image(217, 309, 33, 49).convert()

# Soldier
SOLDIER_SHEET = SNIPER_SHEET  # Both the animations are there in the same sheet

SOLDIER_0 = SOLDIER_SHEET.get_image(22, 4, 37, 40).convert()
SOLDIER_1 = SOLDIER_SHEET.get_image(60, 4, 35, 46).convert()
SOLDIER_2 = SOLDIER_SHEET.get_image(96, 4, 23, 43).convert()
SOLDIER_3 = SOLDIER_SHEET.get_image(121, 4, 29, 43).convert()
SOLDIER_4 = SOLDIER_SHEET.get_image(151, 4, 37, 43).convert()
SOLDIER_5 = SOLDIER_SHEET.get_image(190, 4, 38, 41).convert()
SOLDIER_6 = SOLDIER_SHEET.get_image(231, 4, 29, 45).convert()
SOLDIER_7 = SOLDIER_SHEET.get_image(261, 4, 24, 44).convert()
SOLDIER_8 = SOLDIER_SHEET.get_image(288, 4, 30, 43).convert()

# Tank
TANK_0 = IMG_FOLDER.load_image('tank.png')


# Powerups

POWERUP_SLOW = IMG_FOLDER.load_image('slow.png')
POWERUP_BLINK = IMG_FOLDER.load_image('force.png')
POWERUP_BULLET = IMG_FOLDER.load_image('bullet_slow.png')

# Explosion
EXPLOSION_SHEET = IMG_FOLDER.load_spritesheet('explosion.png')

EXPLOSION_0 = EXPLOSION_SHEET.get_image(0, 0, 31, 30).convert()
EXPLOSION_1 = EXPLOSION_SHEET.get_image(31, 0, 31, 30).convert()
EXPLOSION_2 = EXPLOSION_SHEET.get_image(62, 0, 31, 30).convert()
EXPLOSION_3 = EXPLOSION_SHEET.get_image(93, 0, 31, 30).convert()
EXPLOSION_4 = EXPLOSION_SHEET.get_image(124, 0, 31, 30).convert()


# Sounds
SHOOT_SOUND = SOUND_FOLDER.load_sound('Shoot.wav')
POWERUP_SOUND = SOUND_FOLDER.load_sound('Powerup.wav')
EXPLOSION_SOUND = SOUND_FOLDER.load_sound('Explosion.wav')
HIT_SOUND = SOUND_FOLDER.load_sound('Hit.wav')
JUMP_SOUND = SOUND_FOLDER.load_sound('Jump.wav')
DASH_SOUND = SOUND_FOLDER.load_sound('Dash.wav')

pygame.mixer.music.load(SOUND_FOLDER.get_path('Contra_Contravirt_OC_ReMix.ogv'))
pygame.mixer.music.set_volume(1)
