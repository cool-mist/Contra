# Camera sprite
import pygame
from settings import *
vec = pygame.math.Vector2

class Camera(object):
    def __init__(self, width, height):
    	self.pos = vec(0,0)
    def update(self,sprite):
    	if sprite.canMove:
    		self.pos.x = -sprite.pos.x
    	if self.pos.x >= LEFT_BOUND:
    		self.pos.x = LEFT_BOUND
    	elif self.pos.x <= RIGHT_BOUND:
    		self.pos.x = RIGHT_BOUND
    	#self.pos.y = min(-sprite.pos.y+HEIGHT/2,0)
    	#print(self.pos.x)
   
camera = Camera(WIDTH,HEIGHT)
        
