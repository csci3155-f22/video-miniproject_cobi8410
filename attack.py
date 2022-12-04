import pygame
import os
import random 
import sys
import math

class Attack():
	def __init__(self, anticipation_ids, windup_id, attack_bg_id, recovery_id, anticipation_speeds, windup_speed, attack_speed, recovery_speed, attack_callback):
		self.anticipation_ids = anticipation_ids #ids for boss anticipation animations
		self.windup_id = windup_id #id for boss windup animation
		self.attack_id = attack_id #id for boss attack animation
		self.recovery_id = recovery_id #id for boss recovery animation

		self.anticipation_speeds = anticipation_speeds
		self.windup_speed = windup_speed
		self.attack_speed = attack_speed
		self.recovery_speed = recovery_speed

		self.attacK_callback = attack_callback


#ATTACK DRIVES BOSS THROUGH STATES 2-4

#ATTACK NEEDS

#-ANTICIPATIONS
#	list of anticipations 