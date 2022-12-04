import pygame
import os
import random
from state import *
from player import *
from boss import *

class Game:

	pygame.display.set_caption("barryBee")
	BACKGROUND_COLOR = (0,0,0,0)
	FPS = 60
	clock = pygame.time.Clock()	
	temp_font = pygame.font.SysFont('Arial',12)

	def __init__(self):
		pygame.init()
		pygame.mixer.init()
		pygame.mixer.music.set_volume(0.3)
		
		self.WIDTH, self.HEIGHT = 480, 854
		self.GAME_WIDTH, self.GAME_HEIGHT = 360, 640
		self.WIN = pygame.display.set_mode((self.WIDTH,self.HEIGHT), pygame.SRCALPHA)
		self.game_canvas = pygame.Surface((self.GAME_WIDTH, self.GAME_HEIGHT), pygame.SRCALPHA)
		self.playing = True
		self.running = True
		self.state_stack = [titleState(self)]
		self.prev_state = None
		self.clock = pygame.time.Clock()

		self.player = Player(self.GAME_WIDTH, self.GAME_HEIGHT) #MAKE PLAYER
		self.boss = blackBear((self.GAME_WIDTH, self.GAME_HEIGHT))

	def update(self, events, delta, keys):
		self.state_stack[-1].update(events, delta, keys)

	def render(self, events, delta):
		self.state_stack[-1].render(self.game_canvas, delta)
		self.WIN.blit(pygame.transform.scale(self.game_canvas, (self.WIDTH, self.HEIGHT)),(0,0))
		fps = str(int(Game.clock.get_fps()))
		fps_text = Game.temp_font.render(fps, 1, pygame.Color("coral"))
		self.WIN.blit(fps_text, (10,10)) 
		pygame.display.update()


	def game_loop(self):
		delta = Game.clock.tick(Game.FPS)/1000
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				self.playing = False
				self.running = False

		keys = pygame.key.get_pressed()
		self.update(events, delta, keys)
		self.render(self.WIN, delta)
		if keys[pygame.K_p]:
			pygame.image.save(self.WIN, 'assets/screenshots/screenshot{0}.png'.format(self.screenshot_counter))
			self.screenshot_counter = self.screenshot_counter + 1

