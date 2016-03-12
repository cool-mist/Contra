# Contra with Dash


# Pygame Template

import pygame
import random
import os
from settings import *
from sprites import *
from camera import *
from graphics import *


# Game template class

class Game:
	def __init__(self):		
		# Initialize
		self.screen = screen  # defined in graphics
		pygame.display.set_caption(TITLE)
		self.clock = pygame.time.Clock()
		self.running = True
		self.soldierTimer = SOLDIER_SPAWN_TIMER
		self.reinit()

	def reinit(self):
		self.all_sprites = pygame.sprite.Group()
		self.grounds = pygame.sprite.Group()
		self.player_sprite = pygame.sprite.Group()
		self.bg_sprite = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()
		self.snipers = pygame.sprite.Group()
		self.soldiers = pygame.sprite.Group()
		self.enemy_bullets = pygame.sprite.Group()
		self.tanks = pygame.sprite.Group()
		self.powerups = pygame.sprite.Group()
		self.bosses = pygame.sprite.Group()
		self.death_anims = pygame.sprite.Group()
		self.health = PLAYER_HEALTH
		self.soldierTimer = SOLDIER_SPAWN_TIMER
		self.powerupTimer = POWERUP_TIME
		self.blinkRetract = BLINK_RETRACT
		self.time = 0

	def new(self):
		self.reinit()
		self.run()

	def run(self):
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()
	def deathAnim(self,sprite):
		d = Death(sprite.rect.left,sprite.rect.top)
		self.death_anims.add(d)
		self.all_sprites.add(d)
	def update(self):
		self.time += 1
		if not self.bosses:
			self.playing = False
		self.soldierTimer -= 1
		self.powerupTimer -= 1
		self.soldierTimer %= SOLDIER_SPAWN_TIMER
		if self.soldierTimer == 0:
			self.soldierTimer = SOLDIER_SPAWN_TIMER
			s = Soldier(random.randint(int(p.pos.x+600),int(p.pos.x+800)),random.randint(int(p.pos.y),int(p.pos.y+300)))
			self.soldiers.add(s)
			self.all_sprites.add(s)

		if self.powerupTimer == 0:
			self.powerupTimer = POWERUP_TIME
			po = Powerup(random.randint(int(p.pos.x+300),int(p.pos.x+600)),random.randint(0,3))
			self.powerups.add(po)
			self.all_sprites.add(po)
		self.health = p.health
		self.blinkRetract = p.blinkRetract
		self.all_sprites.update()
		h.update_HUD(self)
		camera.update(p)
		# Check if player fell off screen
		if p.rect.top > HEIGHT or p.rect.x < 0:
			p.die()
			self.deathAnim(p)		
			self.playing = False
		# Check if any enemy dies
		h1 = pygame.sprite.groupcollide(g.bullets,g.snipers,True,True)
		if h1:
			for k in h1:
				self.deathAnim(k)
		h1 = pygame.sprite.groupcollide(g.bullets,g.soldiers,True,True)
		if h1:
			for k in h1:
				self.deathAnim(k)
		h1 = pygame.sprite.groupcollide(g.bullets,g.tanks,True,True)
		if h1:
			for k in h1:
				self.deathAnim(k)

		# Check player colliding with any bullet
		hits = pygame.sprite.spritecollide(p,g.enemy_bullets,True)
		if hits:
			p.health -= 1
			hit_sound.play()
			if p.health == 0:
				p.die()
				self.deathAnim(p)
				self.playing = False

		# or enemy
		h1 = pygame.sprite.spritecollide(p,g.snipers,False)
		if h1:
			p.die()
			self.deathAnim(p)
			self.playing = False
		h1 =  pygame.sprite.spritecollide(p,g.soldiers,False)
		if h1:
			p.die()
			self.deathAnim(p)
			self.playing = False
		h1 = pygame.sprite.spritecollide(p,g.tanks,False)
		if h1:
			p.die()
			self.deathAnim(p)
			self.playing = False


		# Sniper events
		for e in self.snipers:
			b = e.shoot_towards(p)
			if b:
				self.enemy_bullets.add(b)
				self.all_sprites.add(b)

		# Tank Events
		for t in self.tanks:
			b = t.shoot()
			if b:
				self.enemy_bullets.add(b)
				self.all_sprites.add(b)
		# Do not jump up a platform if the full body is not yet above the platform
		hits = pygame.sprite.spritecollide(p,g.grounds,False)
		if hits and p.collisions and p.vel.y <= 0:
			p.collisions = False

		# Enable collisions when body out of ground
		if not hits and not p.collisions:
			p.collisions = True

		# Jump on platform only while falling
		if p.vel.y > 0 and p.collisions:
			if hits:
				p.pos.y = hits[0].defaulty 
				p.stopJumping()
				p.vel.y = 0
				p.canJump = True
		for e in self.soldiers:
			hits = pygame.sprite.spritecollide(e,g.grounds,False)
			if hits :
				e.pos.y = hits[0].defaulty
				e.vel.y = 0

		# Powerup events
		hits = pygame.sprite.spritecollide(p,g.powerups,False)
		if hits:
			powerup = hits[0]
			action = powerup.powerup()
			powerup_sound.play()
			if action == 0:
				p.blinkRetract = 0
				self. blinkRetract = 0
			elif action == 1:
				p.health += 1
				self.health += 1
			else:
				p.drop()
			powerup.kill()

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				if self.playing:
					self.playing = False
				self.running = False
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if not p.dead:
					if event.key == pygame.K_SPACE:
						jump_sound.play()
						p.jump()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if not p.dead:
						b = p.shoot(pygame.mouse.get_pos())
						self.all_sprites.add(b)
						self.bullets.add(b)


	def draw(self):
		# Draw sprites and background on the screen
		self.screen.fill(GREEN)
		self.grounds.draw(self.screen)
		self.bg_sprite.draw(self.screen)
		self.player_sprite.draw(self.screen)
		self.snipers.draw(self.screen)
		self.soldiers.draw(self.screen)
		self.enemy_bullets.draw(self.screen)
		self.bullets.draw(self.screen)
		self.tanks.draw(self.screen)
		self.bosses.draw(self.screen)
		self.powerups.draw(self.screen)
		pygame.draw.rect(self.screen,SEA_BLUE,(0,437,6767,100))
		self.death_anims.draw(self.screen)
		pygame.display.update()

	def draw_text(self, text, size, x, y):
		font_name = pygame.font.match_font('Times')
		font = pygame.font.Font(font_name, size)
		text_surface = font.render(text,True, RED)
		text_rect = text_surface.get_rect()
		text_rect.center = (x,y)
		self.screen.blit(text_surface,text_rect)
		pygame.display.update()

	def show_start_screen(self):
		
		
		waiting_for_start = True
		while waiting_for_start:
			self.screen.blit(ss_background,ss_background.get_rect())
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					waiting_for_start = False
					pygame.quit()
					quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						waiting_for_start = False

	def show_game_over_screen(self):
		text_to_display = "Game Over"
		if not self.bosses:
			text_to_display = "STAGE CLEAR ("+str(int(self.time/FPS))+" s)"
		pygame.draw.rect(self.screen,WHITE,(WIDTH/2, HEIGHT/2 - 35, 200,50))
		self.draw_text(text_to_display, 21, WIDTH/2 + 100, HEIGHT/2 - 20)
		self.draw_text("R to restart, Q to quit", 21,WIDTH/2 + 100, HEIGHT/ 2)

# init game
g = Game()


g.show_start_screen()


g.running = True
while g.running:
	pygame.mixer.music.play(loops = -1)
	# init player
	p = Player(g)
	g.reinit()
	g.player_sprite.add(p)
	g.all_sprites.add(p)


	# init level
	for ground in LEVEL_1:
		gs = Ground(*ground)
		g.all_sprites.add(gs)
		g.grounds.add(gs)

	# init level background based on level
	bg = Background(l1_bg)
	g.bg_sprite.add(bg)
	g.all_sprites.add(bg)

	# init snipers
	for s in LEVEL_1_SNIPERS:
		sn = Sniper(*s)
		g.snipers.add(sn)
		g.all_sprites.add(sn)

	# init soldiers
	for sol in LEVEL_1_SOLDIERS:
		s = Soldier(*sol)
		g.soldiers.add(s)
		g.all_sprites.add(s)

	# init tanks
	for t in LEVEL_1_TANKS:
		tank = Tank(*t)
		g.tanks.add(tank)
		g.all_sprites.add(tank)

	for po in LEVEL_1_PUPS:
		pup = Powerup(*po)
		g.powerups.add(pup)
		g.all_sprites.add(pup)

	# Boss
	for boss in LEVEL_1_BOSSES:
		b = Tank(*boss)
		g.bosses.add(b)
		g.tanks.add(b)
		g.all_sprites.add(b)

	# HUD
	h = HUD()
	g.player_sprite.add(h)
	g.all_sprites.add(h)
	# Start a new game
	g.run()
	g.show_game_over_screen()
	waiting_for_quit_or_restart = True
	while waiting_for_quit_or_restart:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				waiting_for_quit_or_restart = False
				g.running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					waiting_for_quit_or_restart = False
					g.running = False
				if event.key == pygame.K_r:
					waiting_for_quit_or_restart = False

pygame.quit()

