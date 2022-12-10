import pygame
import os
import random

class Particle():

	particle_id = 0
	def __init__(self, x, y, vel_x, vel_y, width, time, color, bg=True, bg_radius=1, bg_color=(255,255,255)):
		self.x, self.y = x, y
		self.vel_x, self.vel_y = vel_x, vel_y
		self.width, self.width_decrease = width, width/time
		self.bg = bg
		self.bg_width = self.width + bg_radius
		self.color, self.bg_color = color, bg_color
		self.id = Particle.particle_id
		Particle.particle_id = Particle.particle_id + 1

	def update(self, delta):
		self.x = self.x + (self.vel_x * 60 * delta)
		self.y = self.y + (self.vel_y * 60 * delta)
		self.width = self.width - (self.width_decrease * 60 * delta)
		self.bg_width = self.bg_width - (self.width_decrease * 60 * delta)

	def render(self, surface):
		if self.bg:
			pygame.draw.circle(surface, self.bg_color, (self.x, self.y), self.bg_width)
		pygame.draw.circle(surface, self.color, (self.x, self.y), self.width)

	def edgeCheck(self, edge_x, edge_y):
		if self.x < 0 or self.x > edge_x:
			return True
		if self.y < 0 or self.y > edge_y:
			return True

		return False

class honeyChargePart(Particle):
	def __init__(self, x, y, vel_x=0, vel_y=random.uniform(-3,-1), width=random.randint(8,12), time=random.randint(15,30), color=(219, 148, 33), bg=True, bg_radius=random.randint(3,7), bg_color=(255,188,48)):
		self.x, self.y = x, y
		self.vel_x, self.vel_y = vel_x, vel_y
		self.width, self.width_decrease = width, width/time
		self.color = color

class RectParticle(Particle):
	def __init__(self, x, y, vel_x, vel_y, width, height, time, color, bg=True, bg_width=2, bg_height=2, bg_color=(255,255,255)):
		self.x, self.y = x, y
		self.vel_x, self.vel_y = vel_x, vel_y
		self.width, self.height = width, height
		self.width_decrease, self.height_decrease = width/time, height/time
		self.rect = pygame.Rect(x-width/2, y-height//2, width, height)
		self.bg = bg
		self.bg_width, self.bg_height = bg_width+width, bg_height+height
		self.bg_rect = pygame.Rect(x-bg_width/2, y-bg_height/2, width+bg_width, height + bg_height)
		self.color, self.bg_color = color, bg_color

	def update(self, delta):
		self.x = self.x + (self.vel_x * 60 * delta)
		self.y = self.y + (self.vel_y * 60 * delta)
		self.width, self.height = self.width - (self.width_decrease * 60 * delta), self.height - (self.height_decrease * 60 * delta)
		self.bg_width, self.bg_height = self.bg_width - (self.width_decrease * 60 * delta), self.bg_height - (self.height_decrease * 60 * delta)

		self.rect.x, self.rect.y = self.x-self.width/2, self.y-self.height/2
		self.bg_rect.x, self.bg_rect.y = self.x-self.bg_width/2, self.y-self.bg_height/2
		self.rect.width, self.bg_rect.width = self.width, self.bg_width
		self.rect.height, self.bg_rect.height = self.height, self.bg_height

	def render(self, surface):
		if self.bg:
			pygame.draw.rect(surface, self.bg_color, self.bg_rect)
		pygame.draw.rect(surface, self.color, self.rect)