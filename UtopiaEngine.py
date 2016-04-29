import random
import numpy as np
import ast
from minigame import *

possible_minigames = ["Search", "Activation", "Connection"]

class Enemy:
	def __init__(self, level, attack, hit, area, spirit = False):
		self.level = level
		self.attack = attack
		self.hit = hit
		self.spirit = spirit
		self.area = area

class Area:
	def __init__(self, number, daytracker, construct, component, treasure, searchbox = 6):
		self.number = number
		self.daytracker = daytracker
		self.construct = construct
		self.component = component
		self.treasure = treasure
class Area1(Area):
	def __init__(self):
		Area.__init__(1, [1, 1, 0, 1, 0, 0], "Seal of Balance", "Silver", "Ice Plate")
		self.enemy1 = Enemy(1, [1], [5, 6], self)
		self.enemy2 = Enemy(2, [1], [6], self)
		self.enemy3 = Enemy(3, [1, 2], [6], self)
		self.enemy4 = Enemy(4, [1, 2, 3], [6], self)
		self.enemy5 = Enemy(5, [1, 2, 3, 4], [6], self)
class Area2(Area):
	def __init__(self):
		Area.__init__(2, [1, 0, 0, 1, 0, 0], "Hermetic Mirror", "Quartz", "Bracelet of Ios")
		self.enemy1 = Enemy(1, [1, 2], [5, 6], self)
		self.enemy2 = Enemy(2, [1], [6], self)
		self.enemy3 = Enemy(3, [1], [6], self)
		self.enemy4 = Enemy(4, [1, 2, 3], [5, 6], self)
		self.enemy5 = Enemy(5, [1, 2, 3, 4], [6], self, True)
class Area3(Area):
	def __init__(self):
		Area.__init__(3, [1, 0, 1, 0, 1, 0], "Void Gate", "Gum", "Shimmering Moonlace")
		self.enemy1 = Enemy(1, [1], [5, 6], self)
		self.enemy2 = Enemy(2, [1, 2], [6], self)
		self.enemy3 = Enemy(3, [1, 2], [6], self)
		self.enemy4 = Enemy(4, [1, 2, 3], [6], self)
		self.enemy5 = Enemy(5, [1, 2, 3, 4], [6], self)
class Area4(Area):
	def __init__(self):
		Area.__init__(4, [1, 0, 1, 0, 1, 0], "Golden Chassis", "Silica", "Scale of the Infinity Wurm")
		self.enemy1 = Enemy(1, [1], [5, 6], self)
		self.enemy2 = Enemy(2, [1], [6], self)
		self.enemy3 = Enemy(3, [1, 2], [6], self, True)
		self.enemy4 = Enemy(4, [1, 2, 3], [6], self)
		self.enemy5 = Enemy(5, [1, 2, 3, 4], [6], self)
class Area5(Area):
	def __init__(self):
		Area.__init__(5, [1, 0, 0, 1, 0, 0], "Scrying Lens", "Wax", "The Ancient Record")
		self.enemy1 = Enemy(1, [1], [5, 6], self)
		self.enemy2 = Enemy(2, [1], [6], self, True)
		self.enemy3 = Enemy(3, [1, 2], [6], self, True)
		self.enemy4 = Enemy(4, [1, 2, 3], [6], self)
		self.enemy5 = Enemy(5, [1, 2, 3, 4], [6], self, True)
class Area6(Area):
	def __init__(self):
		Area.__init__(6, [1, 1, 0, 1, 0, 0], "Crystal Battery", "Lead", "The Molten Shard")
		self.enemy1 = Enemy(1, [1], [5, 6], self)
		self.enemy2 = Enemy(2, [1, 2], [5, 6], self)
		self.enemy3 = Enemy(3, [1, 2, 3], [5, 6], self)
		self.enemy4 = Enemy(4, [1, 2, 3], [6], self, True)
		self.enemy5 = Enemy(5, [1, 2, 3, 4], [6], self, True)

class GameBoard:
	def __init__(self):
		self.area1 = Area1()
		self.area2 = Area2()
		self.area3 = Area3()
		self.area4 = Area4()
		self.area5 = Area5()
		self.area6 = Area6()
		self.possible_areas = [self.area1, self.area2, self.area3, self.area4, self.area5, self.area6]
		self.tools = ["Dowsing Rod", "Paralysis Wand", "Focus Charm"]
		self.construct = {} #dictionary: key->name of construct, value->activation pts
		self.treasure = []
		self.hit = 6
		self.component = {} #dictionary: key->name of component, value->numbers in hold
		self.skull = 8
		self.day = 0
		self.end_day = 22 # when self.day = self.end_day - self.skull, game ends
		self.eventdays = [1, 4, 7, 10, 13, 16, 19]
		self.event = null
		self.events = ["Fleeting visions", "Foul Water", "Good Forture", "Active Monsters"]
		self.godhand = 0 # energy in god hand device
	def eventCycle(self):
		if self.day in self.eventdays:
			self.event = random.choice(self.events)
		else:
			self.event = null
	def take_damage(self, n):
		self.hit = self.hit - n
	def combat(self, enemy):
		damage_taken = 0
		self_dice = 0
		enemy_dice = 0
		while self_dice not in enemy.hit:
			result = roll_dice(2)
			self_dice = result[0]
			enemy_dice = result[1]
			if enemy_dice in enemy.attack:
				damage_taken = damage_taken + 1
		self.take_damage(damage_taken)
		# get_item_or_not = roll_dice(1)
		# if get_item_or_not <= enemy.level:
		# 	if enemy.level == 5:
		# 		return enemy.area.treasure
		# 	else:
		# 		return enemy.area.component
	def rest(self):
		self.day = self.day + 1
		self.hit = self.hit + 1
	def play(self, stretagy):
		while self.day < self.end_day - self.skull:
			self.eventCycle()
			action_to_take = stretagy(possible_minigames)
			if action_to_take == "Search":
				search_game = Search()
				search_area = stretagy(self.possible_areas)
				outcome = search_game.play(stretagy)
				if outcome >= 0 and outcome <= 10: # find construct
					if search_area.construct is None:
						if search_area.component in self.component:
							self.component[search_area.component] += 2
						else:
							self.component[search_area.component] = 2
					else:
						self.construct[search_area.construct] = 0
						search_area.construct = None
				elif outcome >= 11 and outcome <= 99: # find component
					if search_area.component in self.component:
						self.component[search_area.component] += 1
					else:
						self.component[search_area.component] = 1
				elif outcome in range(100, 200) or outcome in range(-100, 0): #combat lv1
					self.combat(search_area.enemy1)
					get_item_or_not = roll_dice(1)
					if get_item_or_not <= 1:
						if search_area.component in self.component:
							self.component[search_area.component] += 1
						else:
							self.component[search_area.component] = 1
				elif outcome in range(200, 300) or outcome in range(-200, -100): #combat lv2
					self.combat(search_area.enemy2)
					get_item_or_not = roll_dice(1)
					if get_item_or_not <= 2:
						if search_area.component in self.component:
							self.component[search_area.component] += 1
						else:
							self.component[search_area.component] = 1
				elif outcome in range(300, 400) or outcome in range(-300, -200): #combat lv3
					self.combat(search_area.enemy3)
					get_item_or_not = roll_dice(1)
					if get_item_or_not <= 3:
						if search_area.component in self.component:
							self.component[search_area.component] += 1
						else:
							self.component[search_area.component] = 1
				elif outcome in range(400, 500) or outcome in range(-400, -300): #combat lv4
					self.combat(search_area.enemy4)
					get_item_or_not = roll_dice(1)
					if get_item_or_not <= 4:
						if search_area.component in self.component:
							self.component[search_area.component] += 1
						else:
							self.component[search_area.component] = 1
				elif outcome in range(500, 556) or outcome in range(-555, -400): #combat lv5
					self.combat(search_area.enemy5)
					get_item_or_not = roll_dice(1)
					if get_item_or_not <= 5:
						if search_area.treasure not in self.treasure:
							self.treasure.append(search_area.treasure)
				if self.hit < 0: #run out of life
					break
				elif self.hit == 0: # rest till restore
					self.rest()
					self.rest()
					self.rest()
					self.rest()
					self.rest()
					self.rest()
			

