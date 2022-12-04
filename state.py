import pygame
import os
import random

pygame.init()
class State():
	def __init__(self, game):
		#pygame.mixer.init()
		self.game = game

	def update(self, events, delta, keys):
		pass

	def render(self, surface, delta):
		pass

	def enter_state(self):
		self.game.state_stack.append(self)

	def exit_state(self):
		self.game.state_stack.pop()

	def reset(self):
		pass

class titleState(State):
	def __init__(self, game):
		self.game = game
		self.bg = pygame.transform.scale(pygame.image.load('assets/screens/title.png'), (self.game.GAME_WIDTH, self.game.GAME_HEIGHT))

	def render(self, surface, delta):
		surface.blit(self.bg, (0,0))
		

	def update(self, events, delta, keys):
		if keys[pygame.K_SPACE]:
			new_state = fightState(self.game, None)
			new_state.enter_state()
			self.game.boss.init_pause_timer = pygame.time.get_ticks()
			self.game.boss.idle_timer = pygame.time.get_ticks()
			

class fightState(State):
	def __init__(self, game, boss):
		self.game = game
		self.game.player.pos[0] = 180
		self.boss = boss
		self.game.boss.init_pause_timer = pygame.time.get_ticks()

		self.bg = pygame.transform.scale(pygame.image.load('assets/stage/test_fight_bg.png'), (self.game.GAME_WIDTH, self.game.GAME_HEIGHT)).convert_alpha()
		self.platform = pygame.transform.scale(pygame.image.load('assets/stage/temp_fight_platform.png'), (self.game.GAME_WIDTH, self.game.GAME_HEIGHT)).convert_alpha()
		self.platform_bg = pygame.transform.scale(pygame.image.load('assets/stage/temp_fight_platform_bg.png'),  (self.game.GAME_WIDTH, self.game.GAME_HEIGHT)).convert_alpha()
		self.trunks_fg = pygame.transform.scale(pygame.image.load('assets/stage/fight_trees_fg.png'), (self.game.GAME_WIDTH*2, self.game.GAME_HEIGHT)).convert_alpha() 
		self.trunks_mg = pygame.transform.scale(pygame.image.load('assets/stage/fight_trees_mg.png'), (self.game.GAME_WIDTH*2, self.game.GAME_HEIGHT)).convert_alpha() 
		self.trunks_bg = pygame.transform.scale(pygame.image.load('assets/stage/fight_trees_bg.png'), (self.game.GAME_WIDTH*2, self.game.GAME_HEIGHT)).convert_alpha() 
		self.god_rays = pygame.image.load('assets/stage/god_rays.png').convert_alpha()
		self.god_rays = pygame.transform.scale(self.god_rays, (self.god_rays.get_width()*2, self.god_rays.get_height()*2))

		self.honey_bar_honey = pygame.image.load('assets/ui/honey_bar_honey.png').convert_alpha()
		self.honey_bar_outline = pygame.image.load('assets/ui/honey_bar_outline.png').convert_alpha()
		self.honey_bar_rect = pygame.Rect(10, (self.game.GAME_HEIGHT-self.honey_bar_honey.get_height())/2, self.honey_bar_outline.get_width(), self.honey_bar_outline.get_height())
		self.honey_bar_cover = pygame.Rect(self.honey_bar_rect.x, self.honey_bar_rect.y+5, self.honey_bar_outline.get_width(), self.honey_bar_outline.get_height()-10)

	def update(self, events, delta, keys):
		self.game.boss.update(delta)
		self.game.player.update(events, delta, keys) 
		self.honey_bar_cover.height = (self.honey_bar_rect.height-10) * (1 - (self.game.player.honey/self.game.player.honey_max))

	def render(self, surface, delta):
		player_offset = (self.game.player.pos[0]-self.game.GAME_WIDTH/2)/10 #player offset, change `10` to change number of parallax instances
		surface.blit(self.bg, (0,0))
		self.doBGParallax(surface, player_offset)
		surface.blit(self.god_rays, (player_offset-30,player_offset-30), special_flags=1)
		attack_mask = self.game.boss.render(surface)
		surface.blit(self.platform_bg, (0,6)) #render platform grass in bg
		self.game.player.render(surface, attack_mask) #render player 
		surface.blit(self.platform, (0,15)) #render platform
		self.renderUI(surface)

	def doBGParallax(self, surface, player_offset):
		fg_offset, mg_offset, bg_offset = 4,2,1 #speed modifiers for layers
		#if player_offset > 10:
			#player_offset = 10
		#if player_offset < -10:
			#player_offset = -10
		surface.blit(self.trunks_bg, (player_offset * bg_offset, 0)) #blit tree layers with offset
		surface.blit(self.trunks_mg, (-30 +player_offset * mg_offset, 0))
		surface.blit(self.trunks_fg, (player_offset * fg_offset - self.game.GAME_WIDTH/2, 0))

	def renderUI(self, surface):
		surface.blit(self.honey_bar_honey, self.honey_bar_rect)
		pygame.draw.rect(surface, (42, 54, 54), self.honey_bar_cover)
		surface.blit(self.honey_bar_outline, self.honey_bar_rect)

