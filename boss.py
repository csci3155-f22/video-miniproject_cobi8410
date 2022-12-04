import pygame
import os
import random 
import sys
import math
from particle import *
from attack import *

class Boss():
	def __init__(self, game_size):
		self.game_size = game_size
		self.idle_sheet = None #sheet for idle animation
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
		self.idle_timer = pygame.timer.get_ticks() #timer to monitor seconds in idle state
		self.idle_duration = 3000 #duration of idle state

		self.init_pause_timer = 0 #timer to pause at start of tight
		self.init_pause_duration = 2000 #duration of start of fight pause
 
	def update(self, delta):
		self.frame = self.frame + (1 * delta * 60) #increase frame

	def render(self, surface):
		active_hitbox = None
		self.surf.fill((0,0,0,0)) #reset surface
		if self.state == 0 or self.state == -1: #if idle
			self.getFrame(self.idle_sheet, 8, 8) #get frame
		elif self.state == 1: #anticipation
			if len (self.current_anticipations) < 1:
				return
			self.getFrame(self.current_anticipations[0]['sheet'], self.current_attack['ant_speed'], self.current_anticipations[0]['frames'])
		elif self.state == 2: #windup
			self.getFrame(self.windup_sheets[self.current_attack['id']], self.current_attack['wind_speed'], self.current_attack['windup_frames'])
		elif self.state == 3: #attack
			self.getFrame(self.attack_sheets[self.current_attack['id']], self.current_attack['atk_speed'], self.current_attack['attack_frames'])
			active_hitbox = self.getMask(self.attack_masks[self.current_attack['id']], self.current_attack['atk_speed'], self.current_attack['attack_frames'])
		elif self.state == 4: #recovery
			self.getFrame(self.recovery_sheets[self.current_attack['id']], self.current_attack['rec_speed'], self.current_attack['recovery_frames'])

		surface.blit(self.surf, (0,0))
		return active_hitbox

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

class blackBear(Boss):
	def __init__(self, game_size):
		self.game_size = game_size 
		self.surf = pygame.Surface(game_size, pygame.SRCALPHA) #surf to blit stuff to

		#ANTICIPATIONS 0-RIGHT EAR (right attack) 1-LEFT EAR (left attack) 2-SNIFF (air attack)
		self.attack_list = self.getAttackList()
		self.anticipation_list = self.getAnticipationList()

		self.windup_sheets = [pygame.transform.scale(pygame.image.load("assets/boss/black_bear_wind_0_sheet.png"), (game_size[0]*self.attack_list[0]['windup_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear_wind_1_sheet.png"), (game_size[0]*self.attack_list[1]['windup_frames'], game_size[1]))]
		self.attack_sheets = [pygame.transform.scale(pygame.image.load("assets/boss/black_bear_atk_0_sheet.png"), (game_size[0]*self.attack_list[0]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear_atk_1_sheet.png"), (game_size[0]*self.attack_list[1]['attack_frames'], game_size[1]))]
		self.attack_masks = [pygame.transform.scale(pygame.image.load("assets/boss/black_bear_atk_0_mask_sheet.png"), (game_size[0]*self.attack_list[0]['attack_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear_atk_1_mask_sheet.png"), (game_size[0]*self.attack_list[1]['attack_frames'], game_size[1]))]
		self.recovery_sheets = [pygame.transform.scale(pygame.image.load("assets/boss/black_bear_rec_0_sheet.png"), (game_size[0]*self.attack_list[0]['recovery_frames'], game_size[1])), pygame.transform.scale(pygame.image.load("assets/boss/black_bear_rec_1_sheet.png"), (game_size[0]*self.attack_list[1]['recovery_frames'], game_size[1]))]
		self.idle_sheet = pygame.transform.scale(pygame.image.load("assets/boss/black_bear_idle_sheet.png"), (game_size[0]*8, game_size[1])).convert_alpha() #sheet for idle animation
		
		self.current_attack = None
		self.current_anticipations = None
		
		self.frame = 0 #frame for animations
		self.state = -1 #0-IDLE, 1-ANTICIPATION, 2-WINDUP, 3-ATTACK, 4-RECOVERY, LOOP TO 0-IDLE,    -1-PRE_FIGHT
		self.STATE_CHANGE_FLAG = False
		self.idle_timer = pygame.time.get_ticks() #timer to monitor seconds in idle state
		self.idle_duration = 3000 #duration of idle state

		self.init_pause_timer = 0 #timer to pause at start of tight
		self.init_pause_duration = 0 #duration of start of fight pause

	def update(self, delta):
		self.frame = self.frame + (1 * delta * 60) #increase frame
		if self.state == -1:
			if pygame.time.get_ticks() - self.init_pause_timer > self.init_pause_duration: #if we have waited 2 seconds
				self.state = 0
		elif self.state == 0: #IDLE state
			if self.current_attack == None: #if we don't have an attack
				self.current_attack = random.choice(self.attack_list) #grab random attack
				self.current_anticipations = [self.anticipation_list[x] for x in self.current_attack['anticipations']] #grab anticipations from attack
			if pygame.time.get_ticks() - self.idle_timer > self.idle_duration: #if idle time is up
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
		
		else: #if still in beginning timeout
			pass

	def getAttackList(self):
		attacks = []

		#ATTACK 0, RIGHT HAND SLAM
		attack0 = {'id':0,'name':'right_hand_slam', 'anticipations':[2, 0], 'windup_frames':6, 'attack_frames':5, 'recovery_frames':4, 'ant_speed':7, 'wind_speed':7, 'atk_speed':5, 'rec_speed':6}
		attacks.append(attack0)
		#ATTACK 1, LEFT HAND SLAM
		attack1 = {'id':1,'name':'left_hand_slam', 'anticipations':[2, 1], 'windup_frames':6, 'attack_frames':5, 'recovery_frames':4, 'ant_speed':7, 'wind_speed':7, 'atk_speed':5, 'rec_speed':6}
		attacks.append(attack1)
		return attacks

	def getAnticipationList(self):
		ancitipations = []
		#ANTICIPATION 0, RIGHT EAR TWITCH, RIGHT SIDE ATTACK
		ancitipations.append({'frames':12, 'sheet':pygame.transform.scale(pygame.image.load("assets/boss/black_bear_ant_0_sheet.png"), (self.game_size[0]*12, self.game_size[1])).convert_alpha()})
		#ANTICIPATION 1, LEFT EAR TWITCH, LEFT SIDE ATTACK
		ancitipations.append({'frames':12, 'sheet':pygame.transform.scale(pygame.image.load("assets/boss/black_bear_ant_1_sheet.png"), (self.game_size[0]*12, self.game_size[1])).convert_alpha()})
		#ANTICIPATION 2, NOSE WIGGLE
		ancitipations.append({'frames':12, 'sheet':pygame.transform.scale(pygame.image.load("assets/boss/black_bear_ant_2_sheet.png"), (self.game_size[0]*12, self.game_size[1])).convert_alpha()})
		return ancitipations





