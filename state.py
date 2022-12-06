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

class fightState(State):
	def __init__(self, game, boss):
		self.game = game
		self.game.player.reset()
		self.game.player.pos[0] = 180
		self.boss = boss
		self.boss.init_pause_timer = pygame.time.get_ticks()
		self.init_time = pygame.time.get_ticks()
		self.rumble_offset = [0,0]
		self.particles = []
		self.percent = 0

		self.bg = pygame.transform.scale(pygame.image.load('assets/stage/test_fight_bg.png'), (self.game.GAME_WIDTH, self.game.GAME_HEIGHT)).convert_alpha()
		self.platform = pygame.transform.scale(pygame.image.load('assets/stage/temp_fight_platform.png'), (self.game.GAME_WIDTH, self.game.GAME_HEIGHT)).convert_alpha()
		self.platform_bg = pygame.transform.scale(pygame.image.load('assets/stage/temp_fight_platform_bg.png'),  (self.game.GAME_WIDTH, self.game.GAME_HEIGHT)).convert_alpha()
		self.trunks_fg = pygame.transform.scale(pygame.image.load('assets/stage/fight_trees_fg.png'), (self.game.GAME_WIDTH*2, self.game.GAME_HEIGHT)).convert_alpha() 
		self.trunks_mg = pygame.transform.scale(pygame.image.load('assets/stage/fight_trees_mg.png'), (self.game.GAME_WIDTH*2, self.game.GAME_HEIGHT)).convert_alpha() 
		self.trunks_bg = pygame.transform.scale(pygame.image.load('assets/stage/fight_trees_bg.png'), (self.game.GAME_WIDTH*2, self.game.GAME_HEIGHT)).convert_alpha() 
		self.god_rays = pygame.image.load('assets/stage/god_rays.png').convert_alpha()
		self.god_rays = pygame.transform.scale(self.god_rays, (self.god_rays.get_width()*2, self.god_rays.get_height()*2))

		self.honey_bar_honey = pygame.image.load('assets/ui/honey_bar_honey_sheet.png').convert_alpha()
		self.honey_bar_outline = pygame.image.load('assets/ui/honey_bar_outline_sheet.png').convert_alpha()
		self.honey_bar_rect = pygame.Rect(10, (self.game.GAME_HEIGHT-self.honey_bar_honey.get_height())/2, self.honey_bar_outline.get_width()/2, self.honey_bar_outline.get_height())
		self.honey_bar_cover = pygame.Rect(self.honey_bar_rect.x, self.honey_bar_rect.y+5, self.honey_bar_outline.get_width()/2, self.honey_bar_outline.get_height()-10)

		self.progress_bar_bg =  pygame.transform.scale(pygame.image.load('assets/ui/progress_bar_bg.png'), (self.game.GAME_WIDTH, self.game.GAME_HEIGHT)).convert_alpha()
		self.progress_bar_flowers = pygame.image.load('assets/ui/progress_bar_flowers.png').convert_alpha()
		self.progress_bee = pygame.image.load('assets/ui/progress_bar_bee.png').convert_alpha()
		self.progress_bar_rect = pygame.Rect((self.game.GAME_WIDTH - self.progress_bar_bg.get_width())/2, 10, self.progress_bar_bg.get_width(), self.progress_bar_bg.get_height())
		self.progress_bar_flowers_rect = pygame.Rect((self.game.GAME_WIDTH - self.progress_bar_flowers.get_width())/2, 0, self.progress_bar_flowers.get_width(), self.progress_bar_flowers.get_height())
		self.progress_bee_rect = pygame.Rect(self.progress_bar_rect.x, self.progress_bar_rect.y+6, self.progress_bee.get_width(), self.progress_bee.get_height())

	def update(self, events, delta, keys):
		self.boss.update(delta)
		self.game.player.update(events, delta, keys) 
		if self.game.player.state != -1:
			self.percent = (pygame.time.get_ticks()-self.init_time)/self.boss.fight_time

		if self.boss.fight_finished: #if boss is done
			end_surf = self.getEndSurf()
			end_surf.fill((64,61,44), special_flags=1)
			new_state = fightEndState(self.game, end_surf, False)
			self.exit_state()
			new_state.enter_state()

		if self.boss.loss_finished:
			end_surf = self.getEndSurf()
			end_surf.fill((64,61,44), special_flags=1)
			new_state = fightEndState(self.game, end_surf, True)
			self.exit_state()
			new_state.enter_state()

		if self.game.player.state == -1: #if player dead
			self.boss.WIN_FLAG = True #set boss state to win
		if self.game.player.fight_end:
			self.boss.LOSE_FLAG = True
			if self.boss.state != -3:
				self.boss.frame = 0
			self.boss.state = -3


		self.honey_bar_cover.height = (self.honey_bar_rect.height-10) * (1 - (self.game.player.honey/self.game.player.honey_max))
		if self.game.player.state != -1:
			if (pygame.time.get_ticks()-self.init_time)/self.boss.fight_time < 1:
				self.progress_bee_rect.x = 26 + (self.game.GAME_WIDTH-26*2 - self.progress_bee.get_width()) * self.percent

		if pygame.time.get_ticks()-self.init_time > self.boss.fight_time: #if fight time is over
			self.boss.vulnerable = True


		if len(self.boss.particles) > 0: #if boss has particles
			self.particles = self.particles + self.boss.particles #add them to our list
		if len(self.particles) > 0:
			for particle in self.particles:
				particle.update(delta)
				if particle.width <= 0 or particle.height <= 0 or particle.edgeCheck(self.game.GAME_WIDTH, self.game.GAME_HEIGHT):
					self.particles.remove(particle)

	def render(self, surface, delta):
		self.getRumble() #get rumble offset
		player_offset = (self.game.player.pos[0]-self.game.GAME_WIDTH/2)/10 #player offset, change `10` to change number of parallax instances
		surface.blit(self.bg, (0 + self.rumble_offset[1],0 + self.rumble_offset[1]))
		self.doBGParallax(surface, player_offset)
		
		attack_mask, vuln_mask = self.boss.render(surface)
		surface.blit(self.platform_bg, (0 + self.rumble_offset[0],6 + self.rumble_offset[1])) #render platform grass in bg
		if len(self.particles) > 0:
			for particle in self.particles:
				particle.render(surface)
		self.game.player.render(surface, attack_mask, vuln_mask) #render player 	
		surface.blit(self.god_rays, (player_offset-30 + self.rumble_offset[0],player_offset-30 + self.rumble_offset[1]), special_flags=1)
		surface.blit(self.platform, (0 + self.rumble_offset[0],15 + self.rumble_offset[1])) #render platform
		self.renderUI(surface)

	def doBGParallax(self, surface, player_offset):
		fg_offset, mg_offset, bg_offset = 4,2,1 #speed modifiers for layers
		#if player_offset > 10:
			#player_offset = 10
		#if player_offset < -10:
			#player_offset = -10
		surface.blit(self.trunks_bg, (player_offset * bg_offset + self.rumble_offset[0], 0 + self.rumble_offset[1])) #blit tree layers with offset
		surface.blit(self.trunks_mg, (-30 +player_offset * mg_offset + self.rumble_offset[0], 0 + self.rumble_offset[1]))
		surface.blit(self.trunks_fg, (player_offset * fg_offset - self.game.GAME_WIDTH/2 + self.rumble_offset[0], 0 + self.rumble_offset[1]))

	def renderUI(self, surface):
		#pygame.draw.rect(surface, (42, 54, 54), self.honey_bar_rect)
		#if self.game.player.state >= 0: #if player alive
		surface.blit(self.honey_bar_honey, self.honey_bar_rect, (0,0,self.honey_bar_honey.get_width()/2, self.honey_bar_honey.get_height()))
		pygame.draw.rect(surface, (42, 54, 54), self.honey_bar_cover)
		surface.blit(self.honey_bar_outline, self.honey_bar_rect, (0,0,self.honey_bar_outline.get_width()/2, self.honey_bar_outline.get_height()))
		#else:
			#pygame.draw.rect(surface, (42,54,54), self.honey_bar_rect)
			#surface.blit(self.honey_bar_honey, self.honey_bar_rect, (self.honey_bar_honey.get_width()/2,0,self.honey_bar_honey.get_width()/2, self.honey_bar_honey.get_height()))
			#surface.blit(self.honey_bar_outline, self.honey_bar_rect, (self.honey_bar_outline.get_width()/2,0,self.honey_bar_outline.get_width()/2, self.honey_bar_outline.get_height()))

		surface.blit(self.progress_bar_bg, self.progress_bar_rect)
		surface.blit(self.progress_bar_flowers, self.progress_bar_flowers_rect, (0,0, self.progress_bar_flowers.get_width()*self.percent, self.progress_bar_flowers.get_height()))
		surface.blit(self.progress_bee, self.progress_bee_rect)

	def getEndSurf(self):
		surface = pygame.Surface((self.game.GAME_WIDTH, self.game.GAME_HEIGHT))
		player_offset = (self.game.player.pos[0]-self.game.GAME_WIDTH/2)/10 #player offset, change `10` to change number of parallax instances
		surface.blit(self.bg, (0,0))
		self.doBGParallax(surface, player_offset)
		surface.blit(self.god_rays, (player_offset-30,player_offset-30), special_flags=1)
		attack_mask = self.boss.render(surface)
		surface.blit(self.platform_bg, (0,6)) #render platform grass in bg
		self.game.player.render(surface, None, None) #render player 	
		surface.blit(self.platform, (0,15)) #render platform

		return surface

	def getRumble(self):
		if self.boss.RUMBLE_FLAG: #if rumbling
			self.rumble_offset = [random.randint(-self.boss.rumble_strength,self.boss.rumble_strength), random.randint(-self.boss.rumble_strength,self.boss.rumble_strength)]
		else:
			self.rumble_offset = [0,0]

class fightEndState(State):
	def __init__(self, game, background, is_win):
		self.game = game
		self.background = background
		self.is_win = is_win
		self.lose_screen, self.win_screen = pygame.image.load('assets/ui/lose_text.png'), pygame.image.load('assets/ui/win_text.png')
		self.init_time = pygame.time.get_ticks()

	def update(self, events, delta, keys):
		if keys[pygame.K_SPACE] and pygame.time.get_ticks()-self.init_time > 2000:
			new_state = titleState(self.game)
			self.exit_state()
			new_state.enter_state()

	def render(self, surface, delta):
		surface.blit(self.background, (0,0))
		if pygame.time.get_ticks()-self.init_time > 1000:
			if self.is_win:
				surface.blit(self.win_screen, (0,0))
			else:
				surface.blit(self.lose_screen, (0,0))

class menuState(State):
	def __init__(self, game):
		self.game = game
		self.bg = None
		self.key_hold_timer = -1
		self.key_accept_hold_time = 1500
		self.cursor_id = 0
		self.max_cursor_id = 2
		self.selected_function = None
		self.cursor = None
		self.cursor_rect_pos = []
		self.button_press = False
		#self.cursor_move_timer = pygame.time.Clock()

	def update(self, events, delta, keys, ):
		self.selected = False
		if keys[pygame.K_SPACE]:
			if pygame.time.get_ticks() - self.key_hold_timer > self.key_accept_hold_time and self.key_hold_timer > 0: #if they have held long enough
				self.selected_function(self.cursor_id)
				return

		for event in events:
			match (event.type, event.__dict__): #pattern match on event type/dict
				case (pygame.KEYDOWN, {'unicode': ' ', 'key': 32, 'mod':_, 'scancode':_, 'window':_}):
					self.key_hold_timer = pygame.time.get_ticks()
				case (pygame.KEYUP, {'unicode': ' ', 'key': 32, 'mod':_, 'scancode':_, 'window':_}):
					if self.key_hold_timer != -1:
						self.cursor_id = (self.cursor_id + 1) % self.max_cursor_id
					self.key_hold_timer = -1

		print(self.key_hold_timer)

	def render(self, surface, delta):
		surface.blit(self.bg, (0,0))
		surface.blit(self.cursor, self.cursor_rect_pos[self.cursor_id])

class bossChoiceState(menuState):
	def __init__(self, game):
		menuState.__init__(self, game)
		self.bg = pygame.image.load('assets/screens/temp_boss_select.png').convert_alpha()
		self.selected_function = self.initiateFight
		self.cursor = pygame.image.load('assets/ui/temp_boss_cursor.png').convert_alpha()
		self.cursor_rect_pos = [((self.game.GAME_WIDTH-self.cursor.get_width())/2,46), ((self.game.GAME_WIDTH-self.cursor.get_width())/2,self.game.GAME_HEIGHT-46-self.cursor.get_height())]

	def initiateFight(self, bear_id):
		bear = self.game.getBoss(bear_id)
		self.cursor_id = 0
		new_state = fightState(self.game, bear)
		new_state.enter_state()

class titleState(menuState):
	def __init__(self, game):
		menuState.__init__(self, game)
		self.bg = pygame.transform.scale(pygame.image.load('assets/screens/title.png'), (self.game.GAME_WIDTH, self.game.GAME_HEIGHT))
		self.selected = False
		self.cursor_rect_pos = [(0,0)]
		self.selected_function = self.exitTitle

	def render(self, surface, delta):
		surface.blit(self.bg, (0,0))

	def exitTitle(self, cursor_id):
		new_state = bossChoiceState(self.game)
		new_state.enter_state()
		
	
