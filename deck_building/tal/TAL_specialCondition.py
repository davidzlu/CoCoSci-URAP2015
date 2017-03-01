import random
import unittest

def generate_special_condition_deck():
	"""Creates and returns a list of every special condition in this file.
	List contains SpecialCondition objects.
	"""
	special_condition_deck = []
	
	
	
	random.shuffle(special_condition_deck)
	return special_condition_deck

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
			pass
			# TODO: add 1 battalion