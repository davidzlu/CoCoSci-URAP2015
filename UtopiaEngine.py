import random
import numpy as np
import ast
from minigame import *

class Enemy:
	def __init__(self, level, attack, hit, spirit = False):
		self.level = level
		self.attack = attack
		self.hit = hit

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
		self.enemy1 = Enemy(1, [1], [5, 6])
		self.enemy2 = Enemy(2, [1], [6])
		self.enemy3 = Enemy(3, [1, 2], [6])
		self.enemy4 = Enemy(4, [1, 2, 3], [6])
		self.enemy5 = Enemy(5, [1, 2, 3, 4], [6])
class Area2(Area):
	def __init__(self):
		Area.__init__(2, [1, 0, 0, 1, 0, 0], "Hermetic Mirror", "Quartz", "Bracelet of Ios")
		self.enemy1 = Enemy(1, [1, 2], [5, 6])
		self.enemy2 = Enemy(2, [1], [6])
		self.enemy3 = Enemy(3, [1], [6])
		self.enemy4 = Enemy(4, [1, 2, 3], [5, 6])
		self.enemy5 = Enemy(5, [1, 2, 3, 4], [6], True)
class Area3(Area):
	def __init__(self):
		Area.__init__(3, [1, 0, 1, 0, 1, 0], "Void Gate", "Gum", "Shimmering Moonlace")
		self.enemy1 = Enemy(1, [1], [5, 6])
		self.enemy2 = Enemy(2, [1, 2], [6])
		self.enemy3 = Enemy(3, [1, 2], [6])
		self.enemy4 = Enemy(4, [1, 2, 3], [6])
		self.enemy5 = Enemy(5, [1, 2, 3, 4], [6])
class Area4(Area):
	def __init__(self):
		Area.__init__(4, [1, 0, 1, 0, 1, 0], "Golden Chassis", "Silica", "Scale of the Infinity Wurm")
		self.enemy1 = Enemy(1, [1], [5, 6])
		self.enemy2 = Enemy(2, [1], [6])
		self.enemy3 = Enemy(3, [1, 2], [6], True)
		self.enemy4 = Enemy(4, [1, 2, 3], [6])
		self.enemy5 = Enemy(5, [1, 2, 3, 4], [6])
class Area5(Area):
	def __init__(self):
		Area.__init__(5, [1, 0, 0, 1, 0, 0], "Scrying Lens", "Wax", "The Ancient Record")
		self.enemy1 = Enemy(1, [1], [5, 6])
		self.enemy2 = Enemy(2, [1], [6], True)
		self.enemy3 = Enemy(3, [1, 2], [6], True)
		self.enemy4 = Enemy(4, [1, 2, 3], [6])
		self.enemy5 = Enemy(5, [1, 2, 3, 4], [6], True)
class Area6(Area):
	def __init__(self):
		Area.__init__(6, [1, 1, 0, 1, 0, 0], "Crystal Battery", "Lead", "The Molten Shard")
		self.enemy1 = Enemy(1, [1], [5, 6])
		self.enemy2 = Enemy(2, [1, 2], [5, 6])
		self.enemy3 = Enemy(3, [1, 2, 3], [5, 6])
		self.enemy4 = Enemy(4, [1, 2, 3], [6], True)
		self.enemy5 = Enemy(5, [1, 2, 3, 4], [6], True)

class GameBoard:
	def __init__(self):
		self.area1 = Area1()
		self.area2 = Area2()
		self.area3 = Area3()
		self.area4 = Area4()