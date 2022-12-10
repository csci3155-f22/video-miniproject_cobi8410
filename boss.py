import pygame
import os
import random 
import sys
import math
import copy
from particle import *
from attack import *

class Boss():
	def __init__(self, game_size):
		self.game_size = game_size
		self.fight_time = 20000
		self.idle_sheet = None #sheet for idle animation
		self.idle_sheet_vulnerable = None
		self.vuln_states = []
		self.attack_sheets = []
		self.attacK_masks
		self.windup_sheets = []
		self.recovery_sheets = []
		self.surf = pygame.Surface(game_size, pygame.SRCALPHA)
		self.attack_list = self.getAttackList()
		self.current_attack = None
		self.anticipation_list = self.getAnticipationList()
		self.frame = 0 #frame for animations
		self.state = 0 #0-IDLE, 1-ANTICIPATION, 2-WINDUP, 3-ATTACK, 4-RECOVERY, LOOP TO 0-IDLE
		self.vulnerable = False #oolean for if we are vulnerable
		self.idle_timer = pygame.timer.get_ticks() #timer to monitor seconds in idle state
		self.idle_duration = 3000 #duration of idle state
		self.fight_finished = False
		self.RUMBLE_FLAG = False
		self.rumble_strength = 5
		self.win_frames = 24

		self.init_pause_timer = 0 #timer to pause at start of tight
		self.init_pause_duration = 2000 #duration of start of fight pause
		self.particles = []

		self.win_flag = None
 
	def update(self, delta):
		self.frame = self.frame + (1 * delta * 60) #increase frame

		if self.win_flag != None: #if win flag has been set
			if self.win_flag: #if its  true
				self.state = -2 #set state to win state
			else: 
				self.state = -3 #set lose state

	def render(self, surface):
		active_hitbox = None
		vuln_mask = None
		self.surf.fill((0,0,0,0)) #reset surface
		if self.state == 0 or self.state == -1: #if idle
			if not self.vulnerable: #if not vulnerable
				self.getFrame(self.idle_sheet, 8, 8) #get frame from idle sheet
			else:
				self.getFrame(self.idle_sheet_vulnerable, 8, 8) #get frame from idle sheet
		elif self.state == 1: #anticipation
			if len (self.current_anticipations) < 1:
				return
			self.getFrame(self.current_anticipations[0]['sheet'], self.current_attack['ant_speed'], self.current_anticipations[0]['frames'])
		elif self.state == 2: #windup
			self.getFrame(self.windup_sheets[self.current_attack['windup']], self.current_attack['wind_speed'], self.current_attack['windup_frames'])
		elif self.state == 3: #attack
			self.getFrame(self.attack_sheets[self.current_attack['id']], self.current_attack['atk_speed'], self.current_attack['attack_frames'])
			active_hitbox = self.getMask(self.attack_masks[self.current_attack['id']], self.current_attack['atk_speed'], self.current_attack['attack_frames'])
		elif self.state == 4: #recovery
			self.getFrame(self.recovery_sheets[self.current_attack['recovery']], self.current_attack['rec_speed'], self.current_attack['recovery_frames'])
		elif self.state == -2: #win
			self.getFrame(self.win_sheet, 10, self.win_frames)
		elif self.state == -3:
			self.getFrame(self.lose_sheet, 10, 24)
		surface.blit(self.surf, (0,0))

		if self.state in self.vuln_states and self.vulnerable: 
			vuln_surf = self.surf.copy()
			vuln_surf.set_colorkey((239,101,68))
			vuln_mask = pygame.mask.from_surface(vuln_surf)
			vuln_mask.invert()

		return active_hitbox, vuln_mask

	def getAttackList(self):
		return []

	def getAnticipationList(self):
		return []

	def getFrame(self, sheet, speed, num_frames):
		index = (self.frame // speed) % num_frames
		width, height = sheet.get_width()/num_frames, sheet.get_height()
		self.surf.blit(sheet, (0,0), (index * width, 0, (index+1) * width, height))
		return index

	def getMask(self, sheet, speed, num_frames):
		mask = pygame.Surface(self.game_size, pygame.SRCALPHA)
		index = (self.frame // speed) % num_frames
		width, height = sheet.get_width()/num_frames, sheet.get_height()
		mask.blit(sheet, (0,0), (index * width, 0, (index+1) * width, height))
		return pygame.mask.from_surface(mask)

class pandaBear(Boss):
	def __init__(self, game_size):
		self.game_size = game_size 
		self.surf = pygame.Surface(game_size, pygame.SRCALPHA) #surf to blit stuff to

		self.attack_list = self.getAttackList()
		self.anticipation_list = self.getAnticipationList()

		self.windup_sheets = [pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_wind_0_sheet.png"), (game_size[0]*self.attack_list[0]['windup_frames'], game_size[1]))]
		self.attack_sheets = [pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_atk_0_sheet.png"), (game_size[0]*self.attack_list[0]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_atk_1_sheet.png"), (game_size[0]*self.attack_list[1]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_atk_2_sheet.png"), (game_size[0]*self.attack_list[2]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_atk_3_sheet.png"), (game_size[0]*self.attack_list[3]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_atk_4_sheet.png"), (game_size[0]*self.attack_list[4]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_atk_5_sheet.png"), (game_size[0]*self.attack_list[5]['attack_frames'], game_size[1]))]
		self.attack_masks = [pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_atk_0_mask_sheet.png"), (game_size[0]*self.attack_list[0]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_atk_1_mask_sheet.png"), (game_size[0]*self.attack_list[1]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_atk_2_mask_sheet.png"), (game_size[0]*self.attack_list[2]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_atk_3_mask_sheet.png"), (game_size[0]*self.attack_list[3]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_atk_4_mask_sheet.png"), (game_size[0]*self.attack_list[4]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_atk_5_mask_sheet.png"), (game_size[0]*self.attack_list[5]['attack_frames'], game_size[1]))]
		self.recovery_sheets = [pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_rec_0_sheet.png"), (game_size[0]*self.attack_list[0]['recovery_frames'], game_size[1]))]
		self.idle_sheet = pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_idle_sheet.png"), (game_size[0]*12, game_size[1])).convert_alpha() #sheet for idle animation
		self.rec_sheet_vulnerable = pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_rec_0_vuln_sheet.png"), (game_size[0]*13, game_size[1])).convert_alpha()
		self.win_sheet = pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_win_sheet.png"), (game_size[0]*20, game_size[1])).convert_alpha() #sheet for win animation
		self.win_frames = 20
		self.lose_sheet = pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_lose_sheet.png"), (game_size[0]*24, game_size[1])).convert_alpha()
		self.current_attack = None
		self.current_anticipations = None
		
		self.frame = 0 #frame for animations
		self.state = -1 #0-IDLE, 1-ANTICIPATION, 2-WINDUP, 3-ATTACK, 4-RECOVERY, LOOP TO 0-IDLE,    -1-PRE_FIGHT, -2-WIN, -3-LOSE, -4-DONE
		self.vulnerable = False
		self.vuln_states = [4]
		self.STATE_CHANGE_FLAG = False
		self.RUMBLE_FLAG = False
		self.WIN_FLAG = False
		self.LOSE_FLAG = False
		self.fight_finished = False
		self.loss_finished = False
		self.fight_time = 35000
		self.idle_timer = pygame.time.get_ticks() #timer to monitor seconds in idle state
		self.idle_duration = 1750 #duration of idle state
		self.rumble_strength = 5

		self.init_pause_timer = 0 #timer to pause at start of tight
		self.init_pause_duration = 0 #duration of start of fight pause

		self.particles = [] #list of particles to be passed to state

	def update(self, delta):
		self.RUMBLE_FLAG = False
		self.frame = self.frame + (1 * delta * 60) #increase frame
		self.particles = []
		if self.state == -1:
			if pygame.time.get_ticks() - self.init_pause_timer > self.init_pause_duration: #if we have waited 2 seconds
				self.state = 0
		elif self.state == 0: #IDLE state
			if self.current_attack == None: #if we don't have an attack
				self.current_attack = random.choice(self.attack_list) #grab random attack
				self.current_anticipations = [self.anticipation_list[x] for x in self.current_attack['anticipations']] #grab anticipations from attack
			if pygame.time.get_ticks() - self.idle_timer > self.idle_duration: #if idle time is up
				if self.WIN_FLAG: #if its  true
					self.state = -2 #set state to win state
				else:
					self.state = 1 #go to anticipation state
				self.frame = 0 #reset frame

		elif self.state == 1: #ANTICIPATION STATE
			index = (self.frame // self.current_attack['ant_speed']) % self.current_anticipations[0]['frames'] #index of anticipation animation
			if index + 1 == self.current_anticipations[0]['frames']: #if we are at end of the anticipation animation
				self.frame = 0 #reset frame
				self.current_anticipations.pop(0) #remove active anticipation from list
				if len(self.current_anticipations) == 0: #if anticipations are finished
					self.state = 2 #move state to windup
					return

		elif self.state == 2: #WINDUP STATE
			index = (self.frame // self.current_attack['wind_speed']) % self.current_attack['windup_frames'] #index of windup animation
			if index + 1 == self.current_attack['windup_frames']: #if we are at end of the windup animation
				self.frame = 0 #reset frame
				self.state = 3 #move state to attack

		elif self.state == 3: #ATTACK STATE
			index = (self.frame // self.current_attack['atk_speed']) % self.current_attack['attack_frames'] #index of attack animation
			
			#get rumbles
			if index in self.current_attack['rumble_frames']: #if we are in rumble frame of attack
				self.RUMBLE_FLAG = True #rumbling

			if index + 1 == self.current_attack['attack_frames']: #if we are at end of the attack animation
				self.frame = 0 #reset frame
				self.state = 4 #move state to recovery 


		elif self.state == 4: #RECOVERY STATE
			index = (self.frame // self.current_attack['rec_speed']) % self.current_attack['recovery_frames'] #index of recovery animation
			if index + 1 == self.current_attack['recovery_frames']: #if we are at end of the recovery animation
				self.frame = 0 #reset frame
				self.state = 0 #reset state to idle
				self.idle_timer = pygame.time.get_ticks()
				self.current_attack = None
				self.current_anticipations = None	 
		
		elif self.state == -2:
			index = (self.frame // 10) % self.win_frames #index of win animation
			if index + 1 == self.win_frames: #if we are at end of the win animation
				self.frame = 0 #reset frame
				self.fight_finished = True #set fight finished flag
				self.idle_timer = pygame.time.get_ticks()
				self.current_attack = None
				self.current_anticipations = None	 
		elif self.state == -3:
			index = (self.frame // 10) % 24 #index of lose animation
			print(index)
			if index + 1 == 24: #if we are at end of the loss animation
				self.frame = self.frame - 1 #reset frame
				self.loss_finished = True #set loss finished flag
				self.idle_timer = pygame.time.get_ticks()
				self.current_attack = None
				self.current_anticipations = None	 
		else: #if still in beginning timeout
			pass


	def render(self, surface):
		active_hitbox = None
		vuln_mask = None
		self.surf.fill((0,0,0,0)) #reset surface
		if self.state == 0 or self.state == -1: #if idle
			self.getFrame(self.idle_sheet, 8, 12) #get frame from idle sheet
		elif self.state == 1: #anticipation
			if len (self.current_anticipations) < 1:
				return
			self.getFrame(self.current_anticipations[0]['sheet'], self.current_attack['ant_speed'], self.current_anticipations[0]['frames'])
		elif self.state == 2: #windup
			self.getFrame(self.windup_sheets[self.current_attack['windup']], self.current_attack['wind_speed'], self.current_attack['windup_frames'])
		elif self.state == 3: #attack
			self.getFrame(self.attack_sheets[self.current_attack['id']], self.current_attack['atk_speed'], self.current_attack['attack_frames'])
			active_hitbox = self.getMask(self.attack_masks[self.current_attack['id']], self.current_attack['atk_speed'], self.current_attack['attack_frames'])
			#surface.blit(self.surf, (0,0), special_flags=4)
			#return active_hitbox, vuln_mask
		elif self.state == 4: #recovery
			if not self.vulnerable: #if not vulnerable
				self.getFrame(self.recovery_sheets[self.current_attack['recovery']], self.current_attack['rec_speed'], self.current_attack['recovery_frames'])
			else:
				self.getFrame(self.rec_sheet_vulnerable, self.current_attack['rec_speed'], self.current_attack['recovery_frames'])
		elif self.state == -2: #win
			self.getFrame(self.win_sheet, 10, self.win_frames)
		elif self.state == -3:
			self.getFrame(self.lose_sheet, 10, 24)
		surface.blit(self.surf, (0,0))

		if self.state in self.vuln_states and self.vulnerable: 
			vuln_surf = self.surf.copy()
			vuln_surf.set_colorkey((239,101,68))
			vuln_mask = pygame.mask.from_surface(vuln_surf)
			vuln_mask.invert()

		return active_hitbox, vuln_mask

	def getAttackList(self):
		attacks = []

		#ATTACK 0, RIGHT HAND SLAM
		attack0 = {'id':0,'name':'right_down_slash', 'anticipations':[0], 'windup':0, 'recovery':0, 'windup_frames':6, 'attack_frames':6, 'recovery_frames':13, 'ant_speed':7, 'wind_speed':7, 'atk_speed':3, 'rec_speed':6, 'rumble_frames': [x for x in range(0,5)]}
		attacks.append(attack0)
		attack1 = {'id':1,'name':'left_down_slash', 'anticipations':[1], 'windup':0, 'recovery':0, 'windup_frames':6, 'attack_frames':6, 'recovery_frames':13, 'ant_speed':7, 'wind_speed':7, 'atk_speed':3, 'rec_speed':6, 'rumble_frames': [x for x in range(0,5)]}
		attacks.append(attack1)
		attack2 = {'id':2,'name':'horizontal_low_slash', 'anticipations':[2], 'windup':0, 'recovery':0, 'windup_frames':6, 'attack_frames':6, 'recovery_frames':13, 'ant_speed':7, 'wind_speed':7, 'atk_speed':3, 'rec_speed':6, 'rumble_frames': [x for x in range(0,5)]}
		attacks.append(attack2)
		attack3 = {'id':3,'name':'horizontal_high_slash', 'anticipations':[3], 'windup':0, 'recovery':0, 'windup_frames':6, 'attack_frames':6, 'recovery_frames':13, 'ant_speed':7, 'wind_speed':7, 'atk_speed':3, 'rec_speed':6, 'rumble_frames': [x for x in range(0,5)]}
		attacks.append(attack3)
		attack4 = {'id':4,'name':'bottom_left_diagonal_slash', 'anticipations':[4], 'windup':0, 'recovery':0, 'windup_frames':6, 'attack_frames':6, 'recovery_frames':13, 'ant_speed':7, 'wind_speed':7, 'atk_speed':3, 'rec_speed':6, 'rumble_frames': [x for x in range(0,5)]}
		attacks.append(attack4)
		attack4 = {'id':5,'name':'top_right_diagonal_slash', 'anticipations':[5], 'windup':0, 'recovery':0, 'windup_frames':6, 'attack_frames':6, 'recovery_frames':13, 'ant_speed':7, 'wind_speed':7, 'atk_speed':3, 'rec_speed':6, 'rumble_frames': [x for x in range(0,5)]}
		attacks.append(attack4)
		"""
		#ATTACK 1, LEFT HAND SLAM
		attack1 = {'id':1,'name':'left_hand_slam', 'anticipations':[1], 'windup':1, 'recovery':1, 'windup_frames':6, 'attack_frames':5, 'recovery_frames':4, 'ant_speed':7, 'wind_speed':7, 'atk_speed':5, 'rec_speed':6, 'rumble_frames': [x for x in range(2,6)]}
		attacks.append(attack1)
		#ATTACK 2, DOUBLE SLAM
		attack2 = {'id':2,'name':'double_slam', 'anticipations':[2, 3], 'windup':2, 'recovery':2, 'windup_frames':6, 'attack_frames':5, 'recovery_frames':4, 'ant_speed':7, 'wind_speed':7, 'atk_speed':5, 'rec_speed':6, 'rumble_frames': [x for x in range(2,6)]}
		attacks.append(attack2)
		#ATTACK 3, RIGHT HAND SWEEP
		attack3 = {'id':3,'name':'right_hand_sweep', 'anticipations':[2, 0], 'windup':3, 'recovery':3, 'windup_frames':5, 'attack_frames':15, 'recovery_frames':5, 'ant_speed':7, 'wind_speed':9, 'atk_speed':3, 'rec_speed':6, 'rumble_frames': [x for x in range(0,16)]}
		attacks.append(attack3)
		#ATTACK 4, LEFT HAND SWEEP
		attack4 = {'id':4,'name':'left_hand_sweep', 'anticipations':[2, 1], 'windup':4, 'recovery':4, 'windup_frames':5, 'attack_frames':15, 'recovery_frames':5, 'ant_speed':7, 'wind_speed':9, 'atk_speed':3, 'rec_speed':6, 'rumble_frames': [x for x in range(0,16)]}
		attacks.append(attack4)
		#ATTACK 5, DOUBLE RIGHT HAND SLAM
		attack5 = {'id':5,'name':'double_right_hand_slam', 'anticipations':[4,0], 'windup':0, 'recovery':0, 'windup_frames':6, 'attack_frames':11, 'recovery_frames':4, 'ant_speed':7, 'wind_speed':7, 'atk_speed':5, 'rec_speed':6, 'rumble_frames': [2,3,4,8,9,10]}
		attacks.append(attack5)
		#ATTACK 6, DOUBLE LEFT HAND SLAM
		attack6 = {'id':6,'name':'double_left_hand_slam', 'anticipations':[4,1], 'windup':1, 'recovery':1, 'windup_frames':6, 'attack_frames':11, 'recovery_frames':4, 'ant_speed':7, 'wind_speed':7, 'atk_speed':5, 'rec_speed':6, 'rumble_frames': [2,3,4,8,9,10]}
		attacks.append(attack6)
		#ATTACK 7, DOUBLE RIGHT HAND SWEEP
		attack7 = {'id':7,'name':'double_right_hand_sweep', 'anticipations':[4,2,0], 'windup':3, 'recovery':5, 'windup_frames':5, 'attack_frames':30, 'recovery_frames':5, 'ant_speed':7, 'wind_speed':9, 'atk_speed':3, 'rec_speed':6, 'rumble_frames': [x for x in range(0,31)]}
		attacks.append(attack7)
		#ATTACK 8, DOUBLE LEFT HAND SWEEP
		attack8 = {'id':8,'name':'double_left_hand_sweep', 'anticipations':[4,2,1], 'windup':4, 'recovery':6, 'windup_frames':5, 'attack_frames':30, 'recovery_frames':5, 'ant_speed':7, 'wind_speed':9, 'atk_speed':3, 'rec_speed':6, 'rumble_frames': [x for x in range(0,31)]}
		attacks.append(attack8)"""
		return attacks

	def getAnticipationList(self):
		ancitipations = []
		#ANTICIPATION 0, RIGHT EAR TWITCH DOWN, RIGHT DOWN SLASH
		ancitipations.append({'frames':22, 'sheet':pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_ant_0_sheet.png"), (self.game_size[0]*22, self.game_size[1])).convert_alpha()})
		#ANTICIPATION 1, LEFT EAR TWITCH DOWN, LEFT DOWN SLASH
		ancitipations.append({'frames':22, 'sheet':pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_ant_1_sheet.png"), (self.game_size[0]*22, self.game_size[1])).convert_alpha()})
		#ANTICIPATION 2, LEFT EAR TWITCH, LEFT SIDE ATTACK
		ancitipations.append({'frames':22, 'sheet':pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_ant_2_sheet.png"), (self.game_size[0]*22, self.game_size[1])).convert_alpha()})
		#ANTICIPATION 3, DOUBLE EAR TWITCH, BOTH SIDE ATTACK
		ancitipations.append({'frames':22, 'sheet':pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_ant_3_sheet.png"), (self.game_size[0]*22, self.game_size[1])).convert_alpha()})
		#ANTICIPATION 4, HAND TAP, DOUBLE ATTACK
		ancitipations.append({'frames':22, 'sheet':pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_ant_4_sheet.png"), (self.game_size[0]*22, self.game_size[1])).convert_alpha()})
		#ANTICIPATION 5, HAND TAP, DOUBLE ATTACK
		ancitipations.append({'frames':22, 'sheet':pygame.transform.scale(pygame.image.load("assets/boss/panda_bear/panda_bear_ant_5_sheet.png"), (self.game_size[0]*22, self.game_size[1])).convert_alpha()})
		return ancitipations



class grizzlyBear(Boss):
	def __init__(self, game_size):
		self.game_size = game_size 
		self.surf = pygame.Surface(game_size, pygame.SRCALPHA) #surf to blit stuff to

		#ANTICIPATIONS 0-RIGHT EAR (right attack) 1-LEFT EAR (left attack) 2-SNIFF (air attack)
		self.attack_list = self.getAttackList()
		self.anticipation_list = self.getAnticipationList()

		self.windup_sheets = [pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_wind_0_sheet.png"), (game_size[0]*self.attack_list[0]['windup_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_wind_1_sheet.png"), (game_size[0]*self.attack_list[1]['windup_frames'], game_size[1])),  pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_wind_2_sheet.png"), (game_size[0]*self.attack_list[2]['windup_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_wind_3_sheet.png"), (game_size[0]*self.attack_list[3]['windup_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_wind_4_sheet.png"), (game_size[0]*self.attack_list[4]['windup_frames'], game_size[1])), ]
		self.attack_sheets = [pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_atk_0_sheet.png"), (game_size[0]*self.attack_list[0]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_atk_1_sheet.png"), (game_size[0]*self.attack_list[1]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_atk_2_sheet.png"), (game_size[0]*self.attack_list[2]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_atk_3_sheet.png"), (game_size[0]*self.attack_list[3]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_atk_4_sheet.png"), (game_size[0]*self.attack_list[4]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_atk_5_sheet.png"), (game_size[0]*self.attack_list[5]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_atk_6_sheet.png"), (game_size[0]*self.attack_list[6]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_atk_7_sheet.png"), (game_size[0]*30, game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_atk_8_sheet.png"), (game_size[0]*30, game_size[1]))]
		self.attack_masks = [pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_atk_0_mask_sheet.png"), (game_size[0]*self.attack_list[0]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_atk_1_mask_sheet.png"), (game_size[0]*self.attack_list[1]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_atk_2_mask_sheet.png"), (game_size[0]*self.attack_list[2]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_atk_3_mask_sheet.png"), (game_size[0]*self.attack_list[3]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_atk_4_mask_sheet.png"), (game_size[0]*self.attack_list[4]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_atk_5_mask_sheet.png"), (game_size[0]*self.attack_list[5]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_atk_6_mask_sheet.png"), (game_size[0]*self.attack_list[6]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_atk_7_mask_sheet.png"), (game_size[0]*30, game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_atk_8_mask_sheet.png"), (game_size[0]*30, game_size[1]))]
		self.recovery_sheets = [pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_rec_0_sheet.png"), (game_size[0]*self.attack_list[0]['recovery_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_rec_1_sheet.png"), (game_size[0]*self.attack_list[1]['recovery_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_rec_2_sheet.png"), (game_size[0]*self.attack_list[2]['recovery_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_rec_3_sheet.png"), (game_size[0]*self.attack_list[3]['recovery_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_rec_4_sheet.png"), (game_size[0]*self.attack_list[4]['recovery_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_rec_5_sheet.png"), (game_size[0]*5, game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_rec_6_sheet.png"), (game_size[0]*5, game_size[1]))]
		self.idle_sheet = pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_idle_sheet.png"), (game_size[0]*8, game_size[1])).convert_alpha() #sheet for idle animation
		self.idle_sheet_vulnerable = pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_idle_vulnerable_sheet.png"), (game_size[0]*8, game_size[1])).convert_alpha()
		self.win_sheet = pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_win_sheet.png"), (game_size[0]*21, game_size[1])).convert_alpha() #sheet for win animation
		self.win_frames = 21
		self.lose_sheet = pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_lose_sheet.png"), (game_size[0]*24, game_size[1])).convert_alpha()
		self.current_attack = None
		self.current_anticipations = None
		
		self.frame = 0 #frame for animations
		self.state = -1 #0-IDLE, 1-ANTICIPATION, 2-WINDUP, 3-ATTACK, 4-RECOVERY, LOOP TO 0-IDLE,    -1-PRE_FIGHT, -2-WIN, -3-LOSE, -4-DONE
		self.vulnerable = False
		self.vuln_states = [0]
		self.STATE_CHANGE_FLAG = False
		self.RUMBLE_FLAG = False
		self.WIN_FLAG = False
		self.LOSE_FLAG = False
		self.fight_finished = False
		self.loss_finished = False
		self.fight_time = 30000
		self.idle_timer = pygame.time.get_ticks() #timer to monitor seconds in idle state
		self.idle_duration = 2000 #duration of idle state
		self.rumble_strength = 5

		self.init_pause_timer = 0 #timer to pause at start of tight
		self.init_pause_duration = 0 #duration of start of fight pause

		self.particles = [] #list of particles to be passed to state

	def update(self, delta):
		self.RUMBLE_FLAG = False
		self.frame = self.frame + (1 * delta * 60) #increase frame
		self.particles = []
		if self.state == -1:
			if pygame.time.get_ticks() - self.init_pause_timer > self.init_pause_duration: #if we have waited 2 seconds
				self.state = 0
		elif self.state == 0: #IDLE state
			if self.current_attack == None: #if we don't have an attack
				self.current_attack = random.choice(self.attack_list) #grab random attack
				self.current_anticipations = [self.anticipation_list[x] for x in self.current_attack['anticipations']] #grab anticipations from attack
			if pygame.time.get_ticks() - self.idle_timer > self.idle_duration: #if idle time is up
				if self.WIN_FLAG: #if its  true
					self.state = -2 #set state to win state
				else:
					self.state = 1 #go to anticipation state
				self.frame = 0 #reset frame

		elif self.state == 1: #ANTICIPATION STATE
			index = (self.frame // self.current_attack['ant_speed']) % self.current_anticipations[0]['frames'] #index of anticipation animation
			if index + 1 == self.current_anticipations[0]['frames']: #if we are at end of the anticipation animation
				self.frame = 0 #reset frame
				self.current_anticipations.pop(0) #remove active anticipation from list
				if len(self.current_anticipations) == 0: #if anticipations are finished
					self.state = 2 #move state to windup
					return

		elif self.state == 2: #WINDUP STATE
			index = (self.frame // self.current_attack['wind_speed']) % self.current_attack['windup_frames'] #index of windup animation
			if index + 1 == self.current_attack['windup_frames']: #if we are at end of the windup animation
				self.frame = 0 #reset frame
				self.state = 3 #move state to attack

		elif self.state == 3: #ATTACK STATE
			index = (self.frame // self.current_attack['atk_speed']) % self.current_attack['attack_frames'] #index of attack animation
			
			#get rumbles
			if index in self.current_attack['rumble_frames']: #if we are in rumble frame of attack
				self.RUMBLE_FLAG = True #rumbling

			if index + 1 == self.current_attack['attack_frames']: #if we are at end of the attack animation
				self.frame = 0 #reset frame
				self.state = 4 #move state to recovery 


		elif self.state == 4: #RECOVERY STATE
			index = (self.frame // self.current_attack['rec_speed']) % self.current_attack['recovery_frames'] #index of recovery animation
			if index + 1 == self.current_attack['recovery_frames']: #if we are at end of the recovery animation
				self.frame = 0 #reset frame
				self.state = 0 #reset state to idle
				self.idle_timer = pygame.time.get_ticks()
				self.current_attack = None
				self.current_anticipations = None	 
		
		elif self.state == -2:
			index = (self.frame // 10) % self.win_frames #index of win animation
			if index + 1 == self.win_frames: #if we are at end of the win animation
				self.frame = 0 #reset frame
				self.fight_finished = True #set fight finished flag
				self.idle_timer = pygame.time.get_ticks()
				self.current_attack = None
				self.current_anticipations = None	 
		elif self.state == -3:
			index = (self.frame // 10) % 24 #index of lose animation
			print(index)
			if index + 1 == 24: #if we are at end of the loss animation
				self.frame = self.frame - 1 #reset frame
				self.loss_finished = True #set loss finished flag
				self.idle_timer = pygame.time.get_ticks()
				self.current_attack = None
				self.current_anticipations = None	 
		else: #if still in beginning timeout
			pass

	def getAttackList(self):
		attacks = []

		#ATTACK 0, RIGHT HAND SLAM
		attack0 = {'id':0,'name':'right_hand_slam', 'anticipations':[0], 'windup':0, 'recovery':0, 'windup_frames':6, 'attack_frames':5, 'recovery_frames':4, 'ant_speed':7, 'wind_speed':7, 'atk_speed':5, 'rec_speed':6, 'rumble_frames': [x for x in range(2,6)]}
		attacks.append(attack0)
		#ATTACK 1, LEFT HAND SLAM
		attack1 = {'id':1,'name':'left_hand_slam', 'anticipations':[1], 'windup':1, 'recovery':1, 'windup_frames':6, 'attack_frames':5, 'recovery_frames':4, 'ant_speed':7, 'wind_speed':7, 'atk_speed':5, 'rec_speed':6, 'rumble_frames': [x for x in range(2,6)]}
		attacks.append(attack1)
		#ATTACK 2, DOUBLE SLAM
		attack2 = {'id':2,'name':'double_slam', 'anticipations':[2, 3], 'windup':2, 'recovery':2, 'windup_frames':6, 'attack_frames':5, 'recovery_frames':4, 'ant_speed':7, 'wind_speed':7, 'atk_speed':5, 'rec_speed':6, 'rumble_frames': [x for x in range(2,6)]}
		attacks.append(attack2)
		#ATTACK 3, RIGHT HAND SWEEP
		attack3 = {'id':3,'name':'right_hand_sweep', 'anticipations':[2, 0], 'windup':3, 'recovery':3, 'windup_frames':5, 'attack_frames':15, 'recovery_frames':5, 'ant_speed':7, 'wind_speed':9, 'atk_speed':3, 'rec_speed':6, 'rumble_frames': [x for x in range(0,16)]}
		attacks.append(attack3)
		#ATTACK 4, LEFT HAND SWEEP
		attack4 = {'id':4,'name':'left_hand_sweep', 'anticipations':[2, 1], 'windup':4, 'recovery':4, 'windup_frames':5, 'attack_frames':15, 'recovery_frames':5, 'ant_speed':7, 'wind_speed':9, 'atk_speed':3, 'rec_speed':6, 'rumble_frames': [x for x in range(0,16)]}
		attacks.append(attack4)
		#ATTACK 5, DOUBLE RIGHT HAND SLAM
		attack5 = {'id':5,'name':'double_right_hand_slam', 'anticipations':[4,0], 'windup':0, 'recovery':0, 'windup_frames':6, 'attack_frames':11, 'recovery_frames':4, 'ant_speed':7, 'wind_speed':7, 'atk_speed':5, 'rec_speed':6, 'rumble_frames': [2,3,4,8,9,10]}
		attacks.append(attack5)
		#ATTACK 6, DOUBLE LEFT HAND SLAM
		attack6 = {'id':6,'name':'double_left_hand_slam', 'anticipations':[4,1], 'windup':1, 'recovery':1, 'windup_frames':6, 'attack_frames':11, 'recovery_frames':4, 'ant_speed':7, 'wind_speed':7, 'atk_speed':5, 'rec_speed':6, 'rumble_frames': [2,3,4,8,9,10]}
		attacks.append(attack6)
		#ATTACK 7, DOUBLE RIGHT HAND SWEEP
		attack7 = {'id':7,'name':'double_right_hand_sweep', 'anticipations':[4,2,0], 'windup':3, 'recovery':5, 'windup_frames':5, 'attack_frames':30, 'recovery_frames':5, 'ant_speed':7, 'wind_speed':9, 'atk_speed':3, 'rec_speed':6, 'rumble_frames': [x for x in range(0,31)]}
		attacks.append(attack7)
		#ATTACK 8, DOUBLE LEFT HAND SWEEP
		attack8 = {'id':8,'name':'double_left_hand_sweep', 'anticipations':[4,2,1], 'windup':4, 'recovery':6, 'windup_frames':5, 'attack_frames':30, 'recovery_frames':5, 'ant_speed':7, 'wind_speed':9, 'atk_speed':3, 'rec_speed':6, 'rumble_frames': [x for x in range(0,31)]}
		attacks.append(attack8)
		return attacks

	def getAnticipationList(self):
		ancitipations = []
		#ANTICIPATION 0, RIGHT EAR TWITCH, RIGHT SIDE ATTACK
		ancitipations.append({'frames':12, 'sheet':pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_ant_0_sheet.png"), (self.game_size[0]*12, self.game_size[1])).convert_alpha()})
		#ANTICIPATION 1, LEFT EAR TWITCH, LEFT SIDE ATTACK
		ancitipations.append({'frames':12, 'sheet':pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_ant_1_sheet.png"), (self.game_size[0]*12, self.game_size[1])).convert_alpha()})
		#ANTICIPATION 2, NOSE WIGGLE
		ancitipations.append({'frames':12, 'sheet':pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_ant_2_sheet.png"), (self.game_size[0]*12, self.game_size[1])).convert_alpha()})
		#ANTICIPATION 3, DOUBLE EAR TWITCH, BOTH SIDE ATTACK
		ancitipations.append({'frames':12, 'sheet':pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_ant_3_sheet.png"), (self.game_size[0]*12, self.game_size[1])).convert_alpha()})
		#ANTICIPATION 4, HAND TAP, DOUBLE ATTACK
		ancitipations.append({'frames':12, 'sheet':pygame.transform.scale(pygame.image.load("assets/boss/grizzly_bear/grizzly_bear_ant_4_sheet.png"), (self.game_size[0]*12, self.game_size[1])).convert_alpha()})
		return ancitipations


class blackBear(Boss):
	def __init__(self, game_size):
		self.game_size = game_size 
		self.surf = pygame.Surface(game_size, pygame.SRCALPHA) #surf to blit stuff to

		#ANTICIPATIONS 0-RIGHT EAR (right attack) 1-LEFT EAR (left attack) 2-SNIFF (air attack)
		self.attack_list = self.getAttackList()
		self.anticipation_list = self.getAnticipationList()

		self.windup_sheets = [pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_wind_0_sheet.png"), (game_size[0]*self.attack_list[0]['windup_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_wind_1_sheet.png"), (game_size[0]*self.attack_list[1]['windup_frames'], game_size[1])),  pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_wind_2_sheet.png"), (game_size[0]*self.attack_list[2]['windup_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_wind_3_sheet.png"), (game_size[0]*self.attack_list[3]['windup_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_wind_4_sheet.png"), (game_size[0]*self.attack_list[4]['windup_frames'], game_size[1]))]
		self.attack_sheets = [pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_atk_0_sheet.png"), (game_size[0]*self.attack_list[0]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_atk_1_sheet.png"), (game_size[0]*self.attack_list[1]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_atk_2_sheet.png"), (game_size[0]*self.attack_list[2]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_atk_3_sheet.png"), (game_size[0]*self.attack_list[3]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_atk_4_sheet.png"), (game_size[0]*self.attack_list[4]['attack_frames'], game_size[1]))]
		self.attack_masks = [pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_atk_0_mask_sheet.png"), (game_size[0]*self.attack_list[0]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_atk_1_mask_sheet.png"), (game_size[0]*self.attack_list[1]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_atk_2_mask_sheet.png"), (game_size[0]*self.attack_list[2]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_atk_3_mask_sheet.png"), (game_size[0]*self.attack_list[3]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_atk_4_mask_sheet.png"), (game_size[0]*self.attack_list[4]['attack_frames'], game_size[1]))]
		self.recovery_sheets = [pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_rec_0_sheet.png"), (game_size[0]*self.attack_list[0]['recovery_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_rec_1_sheet.png"), (game_size[0]*self.attack_list[1]['recovery_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_rec_2_sheet.png"), (game_size[0]*self.attack_list[2]['recovery_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_rec_3_sheet.png"), (game_size[0]*self.attack_list[3]['recovery_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_rec_4_sheet.png"), (game_size[0]*self.attack_list[4]['recovery_frames'], game_size[1]))]
		self.idle_sheet = pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_idle_sheet.png"), (game_size[0]*8, game_size[1])).convert_alpha() #sheet for idle animation
		self.idle_sheet_vulnerable = pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_idle_vulnerable_sheet.png"), (game_size[0]*8, game_size[1])).convert_alpha()
		self.win_sheet = pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_win_sheet.png"), (game_size[0]*24, game_size[1])).convert_alpha() #sheet for win animation
		self.win_frames = 24
		self.lose_sheet = pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_lose_sheet.png"), (game_size[0]*24, game_size[1])).convert_alpha()
		self.current_attack = None
		self.current_anticipations = None
		
		self.frame = 0 #frame for animations
		self.state = -1 #0-IDLE, 1-ANTICIPATION, 2-WINDUP, 3-ATTACK, 4-RECOVERY, LOOP TO 0-IDLE,    -1-PRE_FIGHT, -2-WIN, -3-LOSE, -4-DONE
		self.vulnerable = False
		self.vuln_states = [0]
		self.STATE_CHANGE_FLAG = False
		self.RUMBLE_FLAG = False
		self.WIN_FLAG = False
		self.LOSE_FLAG = False
		self.fight_finished = False
		self.loss_finished = False
		self.fight_time = 20000
		self.idle_timer = pygame.time.get_ticks() #timer to monitor seconds in idle state
		self.idle_duration = 3000 #duration of idle state
		self.rumble_strength = 5

		self.init_pause_timer = 0 #timer to pause at start of tight
		self.init_pause_duration = 0 #duration of start of fight pause

		self.particles = [] #list of particles to be passed to state

	def update(self, delta):
		self.RUMBLE_FLAG = False
		self.frame = self.frame + (1 * delta * 60) #increase frame
		self.particles = []
		if self.state == -1:
			if pygame.time.get_ticks() - self.init_pause_timer > self.init_pause_duration: #if we have waited 2 seconds
				self.state = 0
		elif self.state == 0: #IDLE state
			if self.current_attack == None: #if we don't have an attack
				self.current_attack = random.choice(self.attack_list) #grab random attack
				self.current_anticipations = [self.anticipation_list[x] for x in self.current_attack['anticipations']] #grab anticipations from attack
			if pygame.time.get_ticks() - self.idle_timer > self.idle_duration: #if idle time is up
				if self.WIN_FLAG: #if its  true
					self.state = -2 #set state to win state
				else:
					self.state = 1 #go to anticipation state
				self.frame = 0 #reset frame

		elif self.state == 1: #ANTICIPATION STATE
			index = (self.frame // self.current_attack['ant_speed']) % self.current_anticipations[0]['frames'] #index of anticipation animation
			if index + 1 == self.current_anticipations[0]['frames']: #if we are at end of the anticipation animation
				self.frame = 0 #reset frame
				self.current_anticipations.pop(0) #remove active anticipation from list
				if len(self.current_anticipations) == 0: #if anticipations are finished
					self.state = 2 #move state to windup
					return

		elif self.state == 2: #WINDUP STATE
			index = (self.frame // self.current_attack['wind_speed']) % self.current_attack['windup_frames'] #index of windup animation
			if index + 1 == self.current_attack['windup_frames']: #if we are at end of the windup animation
				self.frame = 0 #reset frame
				self.state = 3 #move state to attack

		elif self.state == 3: #ATTACK STATE
			index = (self.frame // self.current_attack['atk_speed']) % self.current_attack['attack_frames'] #index of attack animation
			
			#get rumbles
			if index > self.current_attack['rumble_frame_begin'] and index < self.current_attack['rumble_frame_end']: #if we are in rumble frame of attack
				self.RUMBLE_FLAG = True #rumbling

			#get particles
			self.particles = self.getParticles()

			if index + 1 == self.current_attack['attack_frames']: #if we are at end of the attack animation
				self.frame = 0 #reset frame
				self.state = 4 #move state to recovery


		elif self.state == 4: #RECOVERY STATE
			index = (self.frame // self.current_attack['rec_speed']) % self.current_attack['recovery_frames'] #index of recovery animation
			if index + 1 == self.current_attack['recovery_frames']: #if we are at end of the recovery animation
				self.frame = 0 #reset frame
				self.state = 0 #reset state to idle
				self.idle_timer = pygame.time.get_ticks()
				self.current_attack = None
				self.current_anticipations = None	 
		
		elif self.state == -2:
			index = (self.frame // 10) % 24 #index of win animation
			if index + 1 == 24: #if we are at end of the win animation
				self.frame = 0 #reset frame
				self.fight_finished = True #set fight finished flag
				self.idle_timer = pygame.time.get_ticks()
				self.current_attack = None
				self.current_anticipations = None	 
		elif self.state == -3:
			index = (self.frame // 10) % 24 #index of lose animation
			print(index)
			if index + 1 == 24: #if we are at end of the loss animation
				self.frame = self.frame - 1 #reset frame
				self.loss_finished = True #set loss finished flag
				self.idle_timer = pygame.time.get_ticks()
				self.current_attack = None
				self.current_anticipations = None	 
		else: #if still in beginning timeout
			pass

	def getAttackList(self):
		attacks = []

		#ATTACK 0, RIGHT HAND SLAM
		attack0 = {'id':0,'name':'right_hand_slam', 'anticipations':[0], 'windup':0, 'recovery':0, 'windup_frames':6, 'attack_frames':5, 'recovery_frames':4, 'ant_speed':7, 'wind_speed':7, 'atk_speed':5, 'rec_speed':6, 'rumble_frame_begin':2, 'rumble_frame_end':5, 'particle_0':RectParticle(0, 620, random.randint(-5,5), random.uniform(-5,-3), random.randint(20,40), random.randint(20,40), random.randint(20,30), (219, 148, 33)), 'particle_0_frame_begin':2, 'particle_0_frame_end':5, 'particle_0_colors':[(113, 68, 28), (77, 44, 23), (129, 123, 26)]}
		attacks.append(attack0)
		#ATTACK 1, LEFT HAND SLAM
		attack1 = {'id':1,'name':'left_hand_slam', 'anticipations':[1], 'windup':1, 'recovery':1, 'windup_frames':6, 'attack_frames':5, 'recovery_frames':4, 'ant_speed':7, 'wind_speed':7, 'atk_speed':5, 'rec_speed':6, 'rumble_frame_begin':2, 'rumble_frame_end':5, 'particle_0':RectParticle(0, 620, random.randint(-5,5), random.uniform(-3,-1), random.randint(20,40), random.randint(20,40), random.randint(20,30), (219, 148, 33)), 'particle_0_frame_begin':2, 'particle_0_frame_end':5, 'particle_0_colors':[(113, 68, 28), (77, 44, 23), (129, 123, 26)]}
		attacks.append(attack1)
		#ATTACK 2, DOUBLE SLAM
		attack2 = {'id':2,'name':'double_slam', 'anticipations':[2, 3], 'windup':2, 'recovery':2, 'windup_frames':6, 'attack_frames':5, 'recovery_frames':4, 'ant_speed':7, 'wind_speed':7, 'atk_speed':5, 'rec_speed':6, 'rumble_frame_begin':2, 'rumble_frame_end':5, 'particle_0':RectParticle(0, 620, 0, random.uniform(-3,-1), random.randint(20,40), random.randint(20,40), random.randint(15,30), (219, 148, 33)), 'particle_0_frame_begin':2, 'particle_0_frame_end':5, 'particle_0_colors':[(113, 68, 28), (77, 44, 23), (129, 123, 26)]}
		attacks.append(attack2)
		#ATTACK 3, RIGHT HAND SWEEP
		attack3 = {'id':3,'name':'right_hand_sweep', 'anticipations':[2, 0], 'windup':3, 'recovery':3, 'windup_frames':5, 'attack_frames':15, 'recovery_frames':5, 'ant_speed':7, 'wind_speed':9, 'atk_speed':3, 'rec_speed':6,'rumble_frame_begin':0, 'rumble_frame_end':15, 'particle_0':RectParticle(0, 620, 0, random.uniform(-3,-1), random.randint(20,40), random.randint(20,40), random.randint(15,30), (219, 148, 33)), 'particle_0_frame_begin':0, 'particle_0_frame_end':15, 'particle_0_colors':[(113, 68, 28), (77, 44, 23), (129, 123, 26)]}
		attacks.append(attack3)
		#ATTACK 4, LEFT HAND SWEEP
		attack4 = {'id':4,'name':'left_hand_sweep', 'anticipations':[2, 1], 'windup':4, 'recovery':4, 'windup_frames':5, 'attack_frames':15, 'recovery_frames':5, 'ant_speed':7, 'wind_speed':9, 'atk_speed':3, 'rec_speed':6,'rumble_frame_begin':0, 'rumble_frame_end':15, 'particle_0':RectParticle(0, 620, 0, random.uniform(-3,-1), random.randint(20,40), random.randint(20,40), random.randint(15,30), (219, 148, 33)), 'particle_0_frame_begin':0, 'particle_0_frame_end':15, 'particle_0_colors':[(113, 68, 28), (77, 44, 23), (129, 123, 26)]}
		attacks.append(attack4)

		return attacks

	def getAnticipationList(self):
		ancitipations = []
		#ANTICIPATION 0, RIGHT EAR TWITCH, RIGHT SIDE ATTACK
		ancitipations.append({'frames':12, 'sheet':pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_ant_0_sheet.png"), (self.game_size[0]*12, self.game_size[1])).convert_alpha()})
		#ANTICIPATION 1, LEFT EAR TWITCH, LEFT SIDE ATTACK
		ancitipations.append({'frames':12, 'sheet':pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_ant_1_sheet.png"), (self.game_size[0]*12, self.game_size[1])).convert_alpha()})
		#ANTICIPATION 2, NOSE WIGGLE
		ancitipations.append({'frames':12, 'sheet':pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_ant_2_sheet.png"), (self.game_size[0]*12, self.game_size[1])).convert_alpha()})
		#ANTICIPATION 3, DOUBLE EAR TWITCH, BOTH SIDE ATTACK
		ancitipations.append({'frames':12, 'sheet':pygame.transform.scale(pygame.image.load("assets/boss/black_bear/black_bear_ant_3_sheet.png"), (self.game_size[0]*12, self.game_size[1])).convert_alpha()})
		return ancitipations

	def getParticles(self):
		particles = []
		index = (self.frame // self.current_attack['atk_speed']) % self.current_attack['attack_frames'] #index of attack animation
		if self.current_attack['id'] == 0 and index > self.current_attack['rumble_frame_begin']: #RIGHT HAND SLAM
			for x in range(50):
				particle = RectParticle( random.randint(-20, 20) + self.game_size[0] - 30, 620, random.randint(-5,5), random.uniform(-5,-3), random.randint(20,40), random.randint(20,40), random.randint(20,30), random.choice(self.current_attack['particle_0_colors']))
				#particle.x =
				#particle.vel_x = random.uniform(-5,5)
				#particle.vel_y = random.uniform(-5,3)
				#particle.color = 
				particles.append(particle)
		elif self.current_attack['id'] == 1 and index > self.current_attack['rumble_frame_begin']:
			for x in range(50):
				#particle = copy.copy(self.current_attack['particle_0'])
				particle = RectParticle(random.randint(-20, 20) + 30, 620, random.randint(-5,5), random.uniform(-5,-3), random.randint(20,40), random.randint(20,40), random.randint(20,30), random.choice(self.current_attack['particle_0_colors']))
				
				#particle.x = random.randint(-20, 20) + 30
				#particle.vel_x = random.uniform(-5,5)
				#particle.vel_y = random.uniform(-5,3)
				#particle.color = random.choice(self.current_attack['particle_0_colors'])
				particles.append(particle)
		elif self.current_attack['id'] == 2 and index > self.current_attack['rumble_frame_begin']:
			for x in range(50):
				particle_l = copy.copy(self.current_attack['particle_0'])
				particle_l.x = random.randint(-20, 20) + self.game_size[0] - 30
				particle_l.vel_x = random.uniform(-5,5)
				particle_l.vel_y = random.uniform(-5,3)
				particle_l.color = random.choice(self.current_attack['particle_0_colors'])

				particle_r = copy.copy(self.current_attack['particle_0'])
				particle_r.x = random.randint(-20, 20) + 30
				particle_r.color = random.choice(self.current_attack['particle_0_colors'])
				particle_r.vel_x = random.uniform(-5,5)
				particle_r.vel_y = random.uniform(-5,3)

				particles.append(particle_l)
				particles.append(particle_r)
		return []







