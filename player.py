import pygame
import os
import random 
import sys
import math
from particle import *

class Player():
	def __init__(self, game_width, game_height):
		self.game_width, self.game_height = game_width, game_height
		
		self.width, self.height = 48,48
		self.pos = [24, 620]
		self.previous_pos = [0,0]
		self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.mask = pygame.mask.from_surface(self.surf)

		self.state = 0 #0-Grounded, 1-Flying
		self.grounded_speed = 3 #Speed on ground
		self.flying_speed = 0
		self.max_downward_speed = 800
		self.max_upward_speed = 10
		self.honey_acceleration = 0.5
		self.fastfall_downward_speed = 22
		self.gravity = 0.3

		self.button_down_time = -1 #Timer for button presses
		self.button_up_time = pygame.time.get_ticks() #Timer for button releases
		self.fastfall_press_timer = pygame.time.Clock() #Clock for double click press
		self.button_release = False
		self.button_press = False
		self.button_hold_timing = 250
		self.direction = 1 #Direction 1: Right -1: Left
		self.frame = 0

		self.honey = 20 #player honey counter
		self.honey_max = 200 #max honey
		self.honey_gain_rate = 1 #gain rate when on ground
		self.honey_lose_rate = 2 #lose rate when boosting
		self.honey_colors = [(255,188,48), (219, 148, 33)] #colors for honey particles
		self.pollen_colors = [(239, 101, 68)] #colors for pollen particles
		self.particles = [] #list of particles

		self.line_timer = pygame.time.get_ticks() #timer for drawing black ticks
		self.line_ticks = []
		self.line_color = (77, 44, 23)

		self.fly_right_sheets = [pygame.transform.scale(pygame.image.load('assets/player/bee_fly_right_0_sheet.png').convert_alpha(), (self.width*4, self.height)),
								pygame.transform.scale(pygame.image.load('assets/player/bee_fly_right_1_sheet.png').convert_alpha(), (self.width*4, self.height)),
								pygame.transform.scale(pygame.image.load('assets/player/bee_fly_right_2_sheet.png').convert_alpha(), (self.width*4, self.height)),
								pygame.transform.scale(pygame.image.load('assets/player/bee_fly_right_3_sheet.png').convert_alpha(), (self.width*4, self.height)),
								pygame.transform.scale(pygame.image.load('assets/player/bee_fly_right_4_sheet.png').convert_alpha(), (self.width*4, self.height))]
		self.fly_left_sheets = [pygame.transform.scale(pygame.image.load('assets/player/bee_fly_left_0_sheet.png').convert_alpha(), (self.width*4, self.height)),
								pygame.transform.scale(pygame.image.load('assets/player/bee_fly_left_1_sheet.png').convert_alpha(), (self.width*4, self.height)),
								pygame.transform.scale(pygame.image.load('assets/player/bee_fly_left_2_sheet.png').convert_alpha(), (self.width*4, self.height)),
								pygame.transform.scale(pygame.image.load('assets/player/bee_fly_left_3_sheet.png').convert_alpha(), (self.width*4, self.height)),
								pygame.transform.scale(pygame.image.load('assets/player/bee_fly_left_4_sheet.png').convert_alpha(), (self.width*4, self.height))]
		self.fly_idle_sheets = [pygame.transform.scale(pygame.image.load('assets/player/bee_fly_idle_0_sheet.png').convert_alpha(), (self.width*4, self.height)),
								pygame.transform.scale(pygame.image.load('assets/player/bee_fly_idle_1_sheet.png').convert_alpha(), (self.width*4, self.height)),
								pygame.transform.scale(pygame.image.load('assets/player/bee_fly_idle_2_sheet.png').convert_alpha(), (self.width*4, self.height)),
								pygame.transform.scale(pygame.image.load('assets/player/bee_fly_idle_3_sheet.png').convert_alpha(), (self.width*4, self.height)),
								pygame.transform.scale(pygame.image.load('assets/player/bee_fly_idle_4_sheet.png').convert_alpha(), (self.width*4, self.height))]
		self.fly_fastfall_image = pygame.transform.scale(pygame.image.load('assets/player/bee_fly_fastfall.png').convert_alpha(), (self.width, self.height))
		self.splat_image = pygame.transform.scale(pygame.image.load('assets/player/bee_splat.png').convert_alpha(), (self.width, self.height))

	def update(self, events, delta, keys):
		self.frame = self.frame + (1 * delta * 60) #increment frame counter
		self.button_release = False #reset button release values
		self.button_press = False #reset button press values
		self.previous_pos[0], self.previous_pos[1] = self.pos[0], self.pos[1]
		#PROCESSING EVENTS
		for event in events:
			match (event.type, event.__dict__): #pattern match on event type/dict
				case (pygame.KEYDOWN, {'unicode': ' ', 'key': 32, 'mod':_, 'scancode':_, 'window':_}): #if space press
					self.button_down_time = pygame.time.get_ticks() #get time since previous
					self.button_press = True
				case (pygame.KEYUP, {'unicode': ' ', 'key': 32, 'mod':_, 'scancode':_, 'window':_}):
					self.button_up_time = pygame.time.get_ticks()
					self.button_release = True
				case _:
					pass

		if self.state == -1:
			pass

		if self.state == 0: #GROUNDED
			self.honey = self.honey + (self.honey_gain_rate * delta * 60) #increase honey for being on ground
			if self.honey > self.honey_max: #cap honey
				self.honey = self.honey_max

			if self.button_release: #if player released button
				self.direction = self.direction * -1
			elif keys[pygame.K_SPACE]: #else if player is holding button
				if pygame.time.get_ticks() - self.button_down_time > self.button_hold_timing and self.button_down_time != -1: #if we held for long enough
					self.state = 1
					self.flying_speed = 1

			#MOVE PLAYER
			self.pos[0] = self.pos[0] + (self.grounded_speed * delta * 60) * self.direction #modify x position w/ dt 

		elif self.state == 1: #FLYING
			for event in events: #looking at events
				match (event.type, event.__dict__): #pattern match
					case (pygame.KEYDOWN, {'unicode': ' ', 'key': 32, 'mod':_, 'scancode':_, 'window':_}): #if space pressed
						if self.fastfall_press_timer.tick() < 200 and self.honey > 0: #if less than 100 ms between last press
							self.state = 2
							if self.flying_speed > 0:
								self.flying_speed = -8
							else:
								self.flying_speed = self.flying_speed - 4
							for x in range(int(self.honey//4)): 
								self.particles.append(Particle(self.pos[0]-22, self.pos[1]-self.height+16, random.uniform(-3,3), random.uniform(-7,-5), random.randint(10,20), random.randint(15,30), random.choice(self.honey_colors)))
								self.particles.append(Particle(self.pos[0]+22, self.pos[1]-self.height+16, random.uniform(-3,3), random.uniform(-7,-5), random.randint(10,20), random.randint(15,30), random.choice(self.honey_colors)))
							self.honey = 0			

			if keys[pygame.K_SPACE] and self.honey > 0 and self.state == 1: #if player holding space:
				self.flying_speed = self.flying_speed + (self.honey_acceleration * delta * 60) #increase velocity
				self.honey = self.honey - (self.honey_lose_rate * delta * 60) #decrease honey
				if self.honey < 0: #cap honey
					self.honey = 0

				for x in range(1):
					self.particles.append(Particle(self.pos[0]-22, self.pos[1]-16, random.randint(-1,1), random.randint(3,5), random.randint(6,10), 30, random.choice(self.honey_colors)))
					self.particles.append(Particle(self.pos[0]+22, self.pos[1]-16, random.randint(-1,1), random.randint(3,5), random.randint(6,10), 30, random.choice(self.honey_colors)))
			
			self.flying_speed = self.flying_speed - (self.gravity * delta * 60) #gravity them
			if self.flying_speed > self.max_upward_speed: #capping max upward velocity
				self.flying_speed = self.max_upward_speed
			if self.flying_speed < -self.max_downward_speed: #capping max downward velocity
				self.flying_speed = -self.max_downward_speed

			self.pos[0] = self.pos[0] + (self.grounded_speed * delta * 60) * self.direction 
			self.pos[1] = self.pos[1] - (self.flying_speed * delta * 60) #modify x position w/ dt 
			if self.groundCheck():
				self.flying_speed = 0

		elif self.state == 2:
			self.flying_speed = self.flying_speed - (self.gravity * delta * 60)
			self.pos[1] = self.pos[1] - (self.flying_speed * delta * 60)
			if self.groundCheck():
				pass

		self.checkEdge() #check collisions
		self.updateRect() #update rectangle to pos


		if pygame.time.get_ticks() - self.line_timer > (50 * 60 * delta) and self.state > -1: #make line every 50 seconds we alive
			self.line_timer = pygame.time.get_ticks() #reset line timer
			self.updateLines(delta)

		if len(self.particles) > 0:
			for particle in self.particles:
				particle.update(delta)
			for particle in self.particles:
				if particle.width <= 0 or particle.x < 9 or particle.x > self.game_width or particle.y > self.game_height:
					self.particles.remove(particle)

	def render(self, surface, attack_mask):
		self.surf.fill((0,0,0,0))
		honey_val = int(self.honey//(self.honey_max/5+1)) #get current honey val (plus one so it doesn't loop to 0)

		if self.state == -1: #SPLAT
			self.surf.blit(self.splat_image, (0,0))
		if self.state == 0: #GROUNDED
			if self.direction == 1: #if we are facing right
				self.getImage(self.fly_right_sheets[honey_val], 8, self.frame) #blit right sheets
			else:
				self.getImage(self.fly_left_sheets[honey_val], 8, self.frame) #blit left sheets

		elif self.state == 1: #AIR
			self.getImage(self.fly_idle_sheets[honey_val], 8, self.frame) #blit idle sheet

		elif self.state == 2:
			self.surf.blit(self.fly_fastfall_image, (0,0))

		self.mask = pygame.mask.from_surface(self.surf)

		for line in self.line_ticks:
			pygame.draw.line(surface, self.line_color, line[0], line[1], width=5)

		surface.blit(self.surf, self.rect) #blit self
		if attack_mask:
			if attack_mask.overlap(self.mask, (self.rect.x, self.rect.y)):
				self.state = -1
		for particle in self.particles:
			particle.render(surface)

	def updateLines(self, delta):
		if self.state != 0:
			x_change, y_change = self.previous_pos[0]- self.pos[0], self.previous_pos[1]-self.pos[1]
			mag = math.sqrt(x_change**2 + y_change**2)
			x_norm, y_norm = int(x_change/mag*3), int(y_change/mag*3)
			new_pos = (self.previous_pos[0]+(x_norm), self.previous_pos[1]+(y_norm)-24)
			self.line_ticks.append(((self.pos[0],self.pos[1]-24), new_pos))
		if len(self.line_ticks) > 7:
			self.line_ticks.pop(0)
		if self.state == 0 and len(self.line_ticks) > 0:
			self.line_ticks.pop(0)

	def updateRect(self): #CHECK EDGE COLLISION
		self.rect.x = self.pos[0]-self.width/2
		self.rect.y = self.pos[1]-self.height	

	def checkEdge(self):
		if (self.pos[0] - self.width/2) < 0:
			self.pos[0] = self.width/2
			self.direction = -1 * self.direction

		elif self.pos[0] + self.width/2 > self.game_width:
			self.pos[0] = self.game_width - self.width/2
			self.direction = -1 * self.direction

		if self.pos[1] < 20:
			self.pos[1] = 20
			self.flying_speed = 0

	def groundCheck(self):
		if self.pos[1] > 621:
			self.pos[1] = 620
			self.state = 0
			return True

	def getImage(self, sheet, speed, frame):
		num_frames = sheet.get_width()/self.width #get number of frames in sheet
		index = (frame // speed) % num_frames #get index of current frame with speed
		self.surf.blit(sheet, (0,0), (index * self.width, 0, (index+1) * self.width, self.height)) #blit frame onto surface