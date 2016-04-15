import random
import numpy as np
import ast
from minigame import *

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
		get_item_or_not = roll_dice(1)
		if get_item_or_not <= enemy.level:
			if enemy.level = 5:
				return enemy.area.treasure
			else:
				return enemy.area.component

