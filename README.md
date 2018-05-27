# <img src="https://i.imgur.com/rUayNwA.png" height = "200px" width ="600px"/>

A 2d side-scroller clone of Contra (1988) game created using python and pygame library.


## Run :runner:

Dependency | Version
---|---
Python | 3.x 32-bit
Pygame | 1.9 32-bit

*Install Python 3 and Pygame 1.9 windows dependencies from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/)* 

```.../Contra/>   python main.py```

*Game tested with above dependencies to work with 32 bit version of Python on Windows.*

## Game Instructions

### Controls :game_die:

Key | Action
---|---
A | Move Left
D | Move Right
S | Drop to a lower platform
R | Quick restart
SPACE | Jump
Left Mouse Button | Shoots in the direction determined by the mouse position
Right Mouse Button |Dash
Mouse Move | Direction of shooting

### Powerups :tropical_drink:

Powerup | Effect
---|---
F | Resets cooldown of Dash
B | +1 Health
Bird | (Powerdown). Causes the player to drop down if taken when on a platform


### Rules

* Get to the end of the Level and defeat the bot tanks
* You will die if you lose all your health
* Each bullet hit will decrease your Health by 1
* Hitting an enemy unit will INSIANTLY KILL you


### Notes on mechanics

* Running soldiers will be difficult to see underwater. (Only their head is visible )
* Jump, Right and Dash for longer distance
* The bird powerup will trigger only if you are walking on a platform while activating.
* Hence jumping directly on top of the powerup will not activate as you are not on a platform. This can be
used to prevent unwanted drops to death
* Trying to drop when on water will cause you to drown and die !!
* Direction of shooting is determined by the mouse position. Mouse above/below the player shoots a bullet at an angle of +/- 45 degrees 
from the ground.
* RMB activates Dash when it is out of cooldown. Its cooldown is depicted in top center of the screen Use this ability to cross broken bridges for example.
* A random powerup drops in front of the player every 2 seconds. If it goes out of screen behind the player, it disappears
* Snipers shoot only when the player is infront of them
* Soldiers who run across the screen are generated randomly every 3 seconds in front of the player
* All global settings are present in the 'settings.py'. They can be changed by the player to make the game more interesting and/or challenging

## Assets

Asset | Credits
---|---
Background | Zephiel87
BGM | Jake Kaufman on [ocremix](https://ocremix.org/)
Sprite sounds | Effects from [bfxr](https://www.bfxr.net/)
Sprites | Google images

# Thank you for playing
