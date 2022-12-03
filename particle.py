import pygame
import os
import random

class Particle():
	def __init__(self, x, y, vel_x, vel_y, width, time, color, bg=True, bg_radius=1, bg_color=(255,255,255)):
		self.x, self.y = x, y
		self.vel_x, self.vel_y = vel_x, vel_y
		self.width, self.width_decrease = width, width/time
		self.bg = bg
		self.bg_width = self.width + bg_radius
		self.color, self.bg_color = color, bg_color

	def update(self, delta):
		self.x = self.x + (self.vel_x * 60 * delta)
		self.y = self.y + (self.vel_y * 60 * delta)
		self.width = self.width - (self.width_decrease * 60 * delta)
		self.bg_width = self.bg_width - (self.width_decrease * 60 * delta)

	def render(self, surface):
		if self.bg:
			pygame.draw.circle(surface, self.bg_color, (self.x, self.y), self.bg_width)
		pygame.draw.circle(surface, self.color, (self.x, self.y), self.width)

class honeyChargePart(Particle):
	def __init__(self, x, y, vel_x=0, vel_y=random.uniform(-3,-1), width=random.randint(8,12), time=random.randint(15,30), color=(219, 148, 33), bg=True, bg_radius=random.randint(3,7), bg_color=(255,188,48)):
		self.x, self.y = x, y
		self.vel_x, self.vel_y = vel_x, vel_y
		self.width, self.width_decrease = width, width/time
		self.color = color
