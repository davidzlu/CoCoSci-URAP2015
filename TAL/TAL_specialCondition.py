import random
from TAL_terrain import *
from TAL_battalions import *
from TAL_situation import *
import unittest

class SpecialCondition:
	def __init__(self):
		self.pool = []

class EmailFromHome:
	"""actively pay 1 SO reduce 2 stress for all pilots"""
	def __init__(self):
		self.type = "active"
	def execute(self, situation, boolean):
		if boolean:
			situation.SOpoints -= 1
			# TODO: all pilots reduce 2 stress

class EnemyReinforcement:
	"""pay 1 SO or add 1 random battalion to enemy rear"""
	def __init__(self):
		self.type = "active"
	def execute(self, situation, boolean):
		if boolean:
			situation.SOpoints -= 1
		else:
			# TODO: add 1 battalion