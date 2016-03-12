# sprites of the game

import pygame
from camera import *
from settings import *
from graphics import *
vec = pygame.math.Vector2


all_sprites = pygame.sprite.Group()

# Player States
RIGHT = 0
LEFT = 1
RIGHT_DOWN = 2
RIGHT_UP = 3
LEFT_UP = 4
LEFT_DOWN = 5

class Player(pygame.sprite.Sprite):
	def __init__(self,game):

		
		pygame.sprite.Sprite.__init__(self)

		# Copy of Game
		self.game = game

		self.image = pygame.transform.scale(PLAYER_RIGHT_0,(PLAYER_WIDTH,PLAYER_HEIGHT))
		self.image.set_colorkey(YELLOW)
		self.rect = self.image.get_rect()
		self.rect.center = (PLAYER_POSX,0)
		self.health = PLAYER_HEALTH

		# Movement
		self.state = RIGHT
		self.up = False
		self.down = False
		self.pos = vec(30,30)
		self.vel = vec(0,0)
		self.acc = vec(0,GRAVITY)
		self.canMove = True
		self.jumping = True
		self.facing = 1

		# Jumping
		self.canJump = False
		self.collisions = True

		# Blinking
		self.blinkTime = BLINK_TIME
		self.canBlink = 1
		self.blinking = False
		self.blinkRetract = BLINK_RETRACT


		self.dead = False
		# Animation
		# Frames hold each frame
		# index determines the current frame to be played
		self.animCounter = ANIM_SPEED

		self.jumpFrames = [PLAYER_JUMP_0,PLAYER_JUMP_1,PLAYER_JUMP_2,PLAYER_JUMP_3]
		self.jumpIndex = 0

		self.rightFrames = [PLAYER_RIGHT_0,PLAYER_RIGHT_1,PLAYER_RIGHT_2,PLAYER_RIGHT_3,PLAYER_RIGHT_4,PLAYER_RIGHT_5]
		self.rightIndex = 0

		self.rightUpFrames = [PLAYER_RIGHT_UP_0,PLAYER_RIGHT_UP_1,PLAYER_RIGHT_UP_2]
		self.rightUpIndex = 0

		self.rightDownFrames =  [PLAYER_RIGHT_DOWN_0,PLAYER_RIGHT_DOWN_1,PLAYER_RIGHT_DOWN_2]
		self.rightDownIndex = 0

		self.deadFrames = [PLAYER_DEAD_0,PLAYER_DEAD_1,PLAYER_DEAD_2,PLAYER_DEAD_3,PLAYER_DEAD_4]
		self.deadIndex = 0

	def update(self):
		self.calcState()
		if self.dead:
			self.kill()
			return
		if self.jumping:
			self.jumpIndex = self.animate(self.jumpFrames,self.jumpIndex,int(PLAYER_HEIGHT/2),PLAYER_WIDTH)
			
		else:
			self.setImageByState()
			if self.isMoving():
				# Set the animation depending on the state
				if self.state == RIGHT:
					self.rightIndex = self.animate(self.rightFrames,self.rightIndex,PLAYER_WIDTH,PLAYER_HEIGHT)
				elif self.state == RIGHT_DOWN:
					self.rightDownIndex = self.animate(self.rightDownFrames,self.rightDownIndex,PLAYER_WIDTH,PLAYER_HEIGHT)
				elif self.state == RIGHT_UP:
					self.rightUpIndex = self.animate(self.rightUpFrames,self.rightUpIndex,PLAYER_WIDTH,PLAYER_HEIGHT)
				elif self.state == LEFT:
					self.rightIndex = self.animate(self.rightFrames,self.rightIndex,PLAYER_WIDTH,PLAYER_HEIGHT,True)
				elif self.state == LEFT_DOWN:
					self.rightDownIndex = self.animate(self.rightDownFrames,self.rightDownIndex,PLAYER_WIDTH,PLAYER_HEIGHT,True)
				elif self.state == LEFT_UP:
					self.rightUpIndex = self.animate(self.rightUpFrames,self.rightUpIndex,PLAYER_WIDTH,PLAYER_HEIGHT,True)
			else:
				# Else a stationary image
				if self.state == RIGHT:
					self.image = pygame.transform.scale(PLAYER_RIGHT_0,(PLAYER_WIDTH,PLAYER_HEIGHT))
				elif self.state == RIGHT_DOWN:
					self.image = pygame.transform.scale(PLAYER_RIGHT_DOWN_0,(PLAYER_WIDTH,PLAYER_HEIGHT))
				elif self.state == RIGHT_UP:
					self.image = pygame.transform.scale(PLAYER_RIGHT_UP_0,(PLAYER_WIDTH,PLAYER_HEIGHT))
				elif self.state == LEFT:
					self.image = pygame.transform.flip(pygame.transform.scale(PLAYER_RIGHT_0,(PLAYER_WIDTH,PLAYER_HEIGHT)),True,False)
				elif self.state == LEFT_DOWN:
					self.image = pygame.transform.flip(pygame.transform.scale(PLAYER_RIGHT_DOWN_0,(PLAYER_WIDTH,PLAYER_HEIGHT)),True,False)
				elif self.state == LEFT_UP:
					self.image = pygame.transform.flip(pygame.transform.scale(PLAYER_RIGHT_UP_0,(PLAYER_WIDTH,PLAYER_HEIGHT)),True,False)
			
		# Blinking and Motion are Disjoint. All others can occur simultaneously
		if self.blinking:
			self.acc = vec(0,0)
			self.vel.y = 0
			self.vel.x = self.facing * BLINK_SPEED
			self.blinkTime -= 1
			self.blinkRetract -= 1
			if self.blinkTime == 0:
				self.blinking = False
				self.blinkTime = BLINK_TIME
				self.blinkRetract = BLINK_RETRACT
		else:
			self.acc = vec(0,GRAVITY)
			if self.blinkRetract == 0 :
				pass
			else:
				self.blinkRetract -= 1
		keystate = pygame.key.get_pressed()
		mousestate = pygame.mouse.get_pressed()
		if keystate[pygame.K_a]:
			self.acc.x = -PLAYER_ACC
			self.facing = -1
		if keystate[pygame.K_d]:
			self.acc.x = PLAYER_ACC
			self.facing = 1
		if keystate[pygame.K_x]:
			self.acc = vec(0,GRAVITY)
			self.vel = vec(0,0)
		if keystate[pygame.K_s]:
			self.drop()
		if mousestate[2]:   # RMB
			if self.canBlink:
				self.blink()
		if not self.pos.x < -LEFT_BOUND and not self.pos.x > -RIGHT_BOUND:
			self.acc.x += self.vel.x * PLAYER_FRC
			self.vel += self.acc
			self.pos += self.vel + 0.5*self.acc	
		else:
			if self.pos.x <= -LEFT_BOUND:
				self.pos.x += 1
			else:
				self.pos.x -= 1
		self.rect.bottom = self.pos.y
		self.image.set_colorkey(YELLOW)
	def isMoving(self):
		if int(self.vel.x):
			return True
		return False

	def jump(self):

		if self.canMove and self.canJump and self.vel.y == 0:
			self.vel.y = -JUMP_HEIGHT
			self.jumping = True
			self.canJump = False

	def blink(self):
		if self.canMove and self.blinkRetract == 0:
			self.blinkRetract = BLINK_RETRACT
			dash_sound.play()
			self.blinking = True

	def stopJumping(self):
		self.jumpIndex = 0
		self.jumping = False

	def animate(self,frames,index,width,height,flip = False):
		self.animCounter -= 1
		if self.animCounter == 0:
			index +=1
			#print(index)
			index %= len(frames)
			if not flip:
				self.image = pygame.transform.scale(frames[index],(width,height))
			else:
				self.image = pygame.transform.flip(pygame.transform.scale(frames[index],(width,height)),True,False)
			self.animCounter = ANIM_SPEED
		rx = self.rect.left
		ry = self.rect.top
		self.rect = self.image.get_rect()
		self.rect.left = rx
		self.rect.top = ry
		return index
	def drop(self):
		if self.canMove:
			self.collisions = False

	def shoot(self,mousePos):
		self.calcState()
		if self.state == RIGHT:
			speedx,speedy = 1,0
			pass
		elif self.state == LEFT:
			speedx,speedy = -1,0
			pass
		elif self.state == RIGHT_UP:
			speedx,speedy = 1,1
			pass
		elif self.state == RIGHT_DOWN:
			speedx,speedy = 1,-1
			pass
		elif self.state == LEFT_UP:
			speedx,speedy = -1,1
			pass
		elif self.state == LEFT_DOWN:
			speedx,speedy = -1,-1
			pass
		shoot_sound.play()
		b = Bullet(PLAYER_POSX,self.pos.y,speedx,speedy)
		return b



	def calcState(self):
		mouseX,mouseY = pygame.mouse.get_pos()

		if mouseY > self.pos.y + BULLET_THRESHOLD:
			self.up = True
			self.down = False
		elif mouseY < self.pos.y - BULLET_THRESHOLD:
			self.up = False
			self.down = True
		else:
			self.up = False
			self.down = False

		if self.facing == 1:
			if self.up:
				self.state = RIGHT_UP
			elif self.down:
				self.state = RIGHT_DOWN
			else:
				self.state = RIGHT
		else:
			if self.up:
				self.state = LEFT_UP
			elif self.down:
				self.state = LEFT_DOWN
			else:
				self.state = LEFT
		
	def setImageByState(self):
		if self.state == RIGHT and not self.isMoving():
			self.image = pygame.transform.scale(PLAYER_RIGHT_0,(PLAYER_WIDTH,PLAYER_HEIGHT))

		self.rect = self.image.get_rect()
		self.rect.left = PLAYER_POSX

	def die(self):
		print("DEAD")
		self.dead = True
		self.health = PLAYER_HEALTH


# Enemies

class Sniper(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((PLAYER_WIDTH,PLAYER_HEIGHT))
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.up = False
		self.down = False
		self.speedy = 0 
		self.defaultx = x
		self.defaulty = y
		self.counter = 60
		self.state = LEFT



	def update(self):
		# Update sprite image based on state 
		if self.state == LEFT:
			self.image = pygame.transform.scale(SNIPER_LEFT,(PLAYER_WIDTH,PLAYER_HEIGHT))
		elif self.state == LEFT_UP:
			self.image = pygame.transform.scale(SNIPER_LEFT_UP,(PLAYER_WIDTH,PLAYER_HEIGHT))
		else:
			self.image = pygame.transform.scale(SNIPER_LEFT_DOWN,(PLAYER_WIDTH,PLAYER_HEIGHT))
		self.image.set_colorkey(YELLOW)
		self.rect.x = self.defaultx + camera.pos.x
		self.rect.y = self.defaulty + camera.pos.y
		pass

	def shoot_towards(self,player):
		#print(str(player.rect.bottom)+","+str(self.rect.bottom))
		if player.rect.top < self.rect.top :
			self.down = True
			self.up = False
			self.state = LEFT_DOWN
		elif player.rect.center[1] > self.rect.bottom :
			self.up = True
			self.down = False
			self.state = LEFT_UP
		else:
			self.up,self.down = False,False
			self.state = LEFT
		if self.rect.x < PLAYER_POSX + SNIPER_RANGE and self.rect.x > PLAYER_POSX :
			if self.counter == 0:
				self.counter = 60
				return self.shoot(self.up,self.down)
			else:
				self.counter -= 1
				return None

	def shoot(self,up,down):
		sx = -1
		if up:
			sy = 1
		elif down:
			sy = -1
		else:
			sy = 0
		b = Bullet(self.rect.left,self.rect.bottom,sx,sy)
		return b

class Soldier(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(SOLDIER_0,(PLAYER_WIDTH,PLAYER_HEIGHT))
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.pos = vec(x,y)
		self.vel = vec(-SOLDIER_SPEEDX,0)
		self.acc = vec(0,GRAVITY)

		# Animation
		self.soldier_frames = [SOLDIER_0,SOLDIER_1,SOLDIER_2,SOLDIER_3,SOLDIER_4,SOLDIER_5,SOLDIER_6,SOLDIER_7,SOLDIER_8]
		self.animIndex = 0
		self.animCounter = ANIM_SPEED

	def animate(self):
		self.animCounter -= 1
		if self.animCounter == 0:
			self.animIndex +=1
			self.animIndex %= len(self.soldier_frames)
			self.image = pygame.transform.scale(self.soldier_frames[self.animIndex],(PLAYER_WIDTH,PLAYER_HEIGHT))
			self.animCounter = ANIM_SPEED
		self.image.set_colorkey(YELLOW)
	def update(self):
		if self.rect.right < 0:
			self.kill()
		self.animate()
		self.vel += self.acc
		self.pos += self.vel + 0.5*self.acc	
		self.rect.x = self.pos.x + camera.pos.x
		self.rect.bottom = self.pos.y + camera.pos.y

	def shoot_towards(self,player):
		# Shoot towards the player.
		pass		

class Tank(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = TANK_0
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.pos = vec(x,y)
		self.counter = 60

	def update(self):
		self.rect.x = self.pos.x + camera.pos.x
		self.counter -= 1
		pass

	def shoot(self):
		if self.rect.x > PLAYER_POSX :
			if self.counter == 0 or self.counter == 5:
				if self.counter == 0:
					self.counter = 60
				return Bullet(self.rect.x,self.rect.bottom,-1,0)
		return None

# Bullet

class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y,speedx,speedy):
		pygame.sprite.Sprite.__init__(self)
		self.image = bulletImage
		self.rect = self.image.get_rect()
		self.image.set_colorkey(WHITE)
		self.rect.left = x
		self.rect.top = y-50
		self.speedx = speedx
		self.speedy = speedy

	def update(self):
		self.rect.left += self.speedx*BULLET_SPEED
		self.rect.top += self.speedy*BULLET_SPEED
		if self.rect.right < 0 or self.rect.left > WIDTH:
			self.kill()


# Platform

class Ground(pygame.sprite.Sprite):
	def __init__(self,x,y,w,h):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((w,h))
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect()
		self.rect.left = x
		self.rect.top = y
		self.defaultx = x
		self.defaulty = y

	def update(self):
		self.rect.x = self.defaultx + camera.pos.x
		#print("Ground : "+str(self.rect.x))
		self.rect.y = self.defaulty + camera.pos.y

# Background Sprite

class Background(pygame.sprite.Sprite):
	def __init__(self,bg):
		pygame.sprite.Sprite.__init__(self)
		self.image = bg
		self.rect = self.image.get_rect()
		self.rect.left = camera.pos.x
		self.rect.y = camera.pos.y

	def update(self):
		self.rect.x = camera.pos.x
		self.rect.y = camera.pos.y

class HUD(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		pygame.font.init()
		self.surface = pygame.Surface((WIDTH,40))
		self.surface.fill(WHITE)
		self.image = self.surface
		self.rect = self.image.get_rect()
		self.rect.left = 0
		self.rect.top = 0
		self.font = pygame.font.SysFont("monospace", 20)

	# Health indicator
	# Bullets indicator
	# Powerup indicator
	# Blink Indicator
	def update(self):
		pass

	def update_HUD(self,game):
		self.surface = pygame.Surface((WIDTH,30))
		self.surface.fill(LIGHT_YELLOW)
		self.drawHealth(game.health)
		self.drawBlink(game.blinkRetract)
		self.drawPowerup()
		pass

	def drawHealth(self,health):
		if health > PLAYER_HEALTH - 5:
			text = self.font.render("Health: "+str(health), 1,DARK_GREEN)
		elif health > 10:
			text = self.font.render("Health: "+str(health), 1,DARK_YELLOW)
		else:
			text = self.font.render("Health: "+str(health), 1,RED)
		textPos = text.get_rect()
		textPos.centerx = 130
		self.surface.blit(text,textPos)
		self.image = self.surface

	def drawBlink(self,retract):
		retractPerc = str(100 - int(retract/BLINK_RETRACT*100))
		if retractPerc == '100':
			retractPerc = "ONLINE"
			text = self.font.render("Dash: "+retractPerc, 1,DARK_GREEN)
		else:
			text = self.font.render("Dash: "+retractPerc, 1,RED)
		textPos = text.get_rect()
		textPos.centerx = 410
		self.surface.blit(text,textPos)
		self.image = self.surface

	def drawPowerup(self):
		pass





class Powerup(pygame.sprite.Sprite):
	def __init__(self,x,ptype):
		pygame.sprite.Sprite.__init__(self)
		if ptype == 1:
			self.image = POWERUP_BULLET
		elif ptype == 0:
			self.image = POWERUP_BLINK
		else:
			self.image = POWERUP_SLOW
		self.rect = self.image.get_rect()
		self.image.set_colorkey(BLACK)
		if x > 6164:
			x = 6160
		self.rect.x = x
		self.defaultx = x
		self.rect.y = -5
		
		self.ptype = ptype

	def update(self):
		if not self.rect.y >= 170:
			self.rect.y += POWERUP_SPEED

		self.rect.x = camera.pos.x + self.defaultx
		if self.rect.x < 0:
			self.kill()

	def powerup(self):
		# perform the action of the powerup
		return self.ptype
		pass


# Death Animation Sprite
class Death(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = EXPLOSION_0
		self.rect = self.image.get_rect()
		self.rect.left = x
		self.defaultx = x
		self.rect.top = y 
		self.time = 0
		self.image.set_colorkey(WHITE)
		self.explosionFrames = [EXPLOSION_0,EXPLOSION_1,EXPLOSION_2,EXPLOSION_3,EXPLOSION_4]
		explosion_sound.play()
	def update(self):
		#self.rect.left = self.defaultx + camera.pos.x
		self.time += 1
		if self.time == 5:
			self.kill()
			return
		self.image = self.explosionFrames[self.time]
		self.image.set_colorkey(WHITE)
		
		pass

