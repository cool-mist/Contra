""" Holds the settings """
import os
from utils import GameResources

# Project Properties
TITLE = "Contra"
WIDTH = 600
HEIGHT = 480
WINDOW_SIZE = (WIDTH, HEIGHT)
FPS = 60

# Camera
CAMERA_LEFT_BOUDN = 0
CAMERA_RIGHT_BOUND = -6164

# Assets
GAME_FOLDER = GameResources(os.path.dirname(__file__))
IMG_FOLDER = GAME_FOLDER.get_resource("img")
SOUND_FOLDER = GAME_FOLDER.get_resource("sounds")

# Player Settings
PLAYER_HEALTH = 20
PLAYER_POSX = 100
PLAYER_ACC = 0.5
PLAYER_FRC = -0.12
PLAYER_WIDTH = 35
PLAYER_HEIGHT = 55
GRAVITY = 1
JUMP_HEIGHT = 15
BLINK_TIME = 10
BLINK_DISTANCE = 300
BLINK_SPEED = 20
BLINK_RETRACT = 500
ANIM_SPEED = 5  # Lower the faster

# Powerups
POWERUP_SPEED = 10
POWERUP_TIME = 300

# Bullet
BULLET_SPEED = 10
BULLET_THRESHOLD = 50

# Sniper
SNIPER_RANGE = 500

LEVEL_1_SNIPERS = [(511, 286),
                   (695, 292),
                   (1443, 162),
                   (2702, 100),
                   (2767, 345),
                   (3150, 218),
                   (4146, 251),
                   (4652, 153),
                   (5210, 243),
                   (5710, 344),
                   (6469, 284)
                   ]

# Soldier
SOLDIER_SPEEDX = 5
SOLDIER_SPAWN_TIMER = 120

LEVEL_1_SOLDIERS = [(500, 10)]

# Tank
TANK_WIDTH = 100
TANK_HEIGHT = 60


LEVEL_1_TANKS = [
    (3620, 119),
    (3492, 244),
    (5015, 297),
    (5610, 231),
    (5882, 302),
    (6336, 364),
    (6327, 178)
]

# platforms
PLATFORM_THICKNESS = 1
pt = PLATFORM_THICKNESS

# LEVEL_1
LEVEL_1 = [(-200, HEIGHT-pt, WIDTH*20, pt),
           (570, 407, 110, pt),
           (500, 340, 55, pt),
           (690, 340, 55, pt),
           (312, 283, 180, pt),
           (62, 217, 1430, pt),
           (814, 280, 110, pt),
           (1194, 404, 110, pt),
           (1255, 313, 175, pt),
           (1765, 223, 300, pt),  # First Blink
           (2320, 223, 490, pt),
           (2765, 410, 175, pt),
           (2698, 155, 996, pt),
           (2950, 320, 117, pt),
           (3141, 270, 410, pt),
           (3389, 406, 370, pt),
           (3681, 218, 390, pt),
           (3765, 345, 120, pt),
           (3952, 344, 120, pt),
           (4013, 153, 310, pt),
           (4140, 312, 55, pt),
           (4264, 280, 180, pt),
           (4390, 218, 120, pt),  # First Discontinuity
           (4575, 405, 12, pt),
           (4575, 278, 120, pt),
           (4639, 216, 120, pt),  # Second Discontinuity
           (4829, 405, 55, pt),
           (4828, 277, 120, pt),
           (4891, 343, 180, pt),
           (5081, 218, 120, pt),
           (5143, 406, 55, pt),
           (5142, 155, 120, pt),
           (5206, 312, 55, pt),   # Third Discontinuity
           (5332, 218, 120, pt),
           (5392, 281, 310, pt),
           (5582, 408, 180, pt),  # Fourth Discontinuity
           (5832, 344, 120, pt),  # Final Discontinuity
           (6020, 281, 120, pt),
           (6146, 218, 240, pt),
           (6146, 406, 400, pt),
           (6208, 312, 180, pt),
           (6396, 280, 55, pt),
           (6460, 342, 55, pt),
           # Boss
           ]
LEVEL_1_BG = 'l1.png'

LEVEL_1_PUPS = [
    (1908, 3)
]

LEVEL_1_BOSSES = [
    (6616, 83),
    (6658, 171),
    (6616, 258),
    (6658, 352)
]
