import random
from TAL_terrain import *
from TAL_campaigns import *
from TAL_situation import *
import unittest

def get_enemy_units(list_unittype_num):
	"""construct a list of enemy units in battalion using a list of [unit type, nums of units] sublists"""
	enemy_unit = []
	for element in list_unittype_num:
		for i in range(0, element[1]):
			enemy_unit.append(element[0])
	return enemy_unit

class MobileHQ:
	def __init__(self):
		self.vp = 2
		self.type = (3, "C")
		self.units = get_enemy_units([["AAA", 2], ["APC", 2], ["Commands", 4], ["SCUD", 2], ["SPA", 2], ["Truck", 2]])
		self.half_value = 16
		self.destroy_value = 5
		"""TODO list: special note here"""

class InfantryForce:
	def __init__(self):
		self.vp = 5
		self.type = (1, "A")
		self.units = get_enemy_units([["AAA", 4], ["APC", 5], ["Commands", 2], ["Infantry", 10], ["Truck", 4]])
		self.half_value = 20
		self.destroy_value = 5

class TestMethods(unittest.TestCase):
	def test_get_enemy_units_mobile_HQ(self):
		self.assertTrue(MobileHQ().units == ["AAA", "AAA", "APC", "APC", "Commands", 
			"Commands", "Commands", "Commands", "SCUD", "SCUD", "SPA", "SPA", "Truck", "Truck"])

	def test_get_enemy_units_InfantryForce(self):
		self.assertTrue(InfantryForce().units == ["AAA", "AAA", "AAA", "AAA", "APC", "APC", "APC", "APC", "APC",
			"Commands", "Commands", "Infantry", "Infantry", "Infantry", "Infantry", "Infantry", "Infantry", "Infantry",
			"Infantry", "Infantry", "Infantry", "Truck", "Truck", "Truck", "Truck"])


if __name__ == '__main__':
    unittest.main()