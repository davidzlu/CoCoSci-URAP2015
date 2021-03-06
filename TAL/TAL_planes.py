import random
from TAL_terrain import *
from TAL_battalions import *
from TAL_situation import *
from TAL_pilots import *
import unittest

class A_10A:
	def __init__(self):
		self.year = 1976
		self.cannon = 4
		self.so = 8
		self.hit = 3
		"""TODO: weapon list"""
		self.weight = 14

class AH_1:
	def __init__(self):
		self.year = 1967
		self.cannon = 9
		self.so = 2
		self.hit = 1
		"""TODO: weapon list"""
		self.weight = 6

class F_16:
	def __init__(self):
		self.year = 1976
		self.cannon = 7
		self.so = 5
		self.hit = 2
		"""TODO: weapon list"""
		self.weight = 10

class AH_64A:
	def __init__(self):
		self.year = 1986
		self.cannon = 7
		self.so = 4
		self.hit = 2
		"""TODO: weapon list"""
		self.weight = 8

class AV_8B:
	def __init__(self):
		self.year = 1985
		self.cannon = 7
		self.so = 6
		self.hit = 2
		"""TODO: weapon list"""
		self.weight = 10

class A_10C:
	def __init__(self):
		self.year = 2006
		self.cannon = 4
		self.so = 9
		self.hit = 3
		"""TODO: weapon list"""
		self.weight = 14

class MQ_1:
	def __init__(self):
		self.year = 2001
		self.cannon = 0
		self.so = 4
		self.hit = 0
		"""TODO: weapon list"""
		self.weight = 0

class RQ_1:
	def __init__(self):
		self.year = 1995
		self.cannon = 0
		self.so = 4
		self.hit = 0
		"""TODO: weapon list"""
		self.weight = 0

class AH_64D:
	def __init__(self):
		self.year = 1997
		self.cannon = 7
		self.so = 5
		self.hit = 2
		"""TODO: weapon list"""
		self.weight = 8

class AC_130:
	def __init__(self):
		self.year = 1995
		self.cannon = 5 # or 3 or 1
		self.so = 10
		self.hit = 3
		"""TODO: special effect"""
		self.weight = 0

plane_pool = {A_10A: 4, AH_1: 3, F_16: 1, AH_64A: 8, AV_8B: 3, A_10C: 2, MQ_1: 2, RQ_1: 2, AH_64D: 4, AC_130: 1}

def legal_actions(campaign):
	possible_choices = []
	for plane in plane_pool.keys():
		if plane().year <= campaign.year and plane_pool[plane] > 0:
			possible_choices.append(plane)
	return possible_choices

def get_all_planes(campaign, situation, pick_strategy, determine_strategy):
	planes = []
	to_pick_or_not = True
	while to_pick_or_not:
		planes_so = 0
		if planes != None:
			planes_so = sum([p.so for p in planes])
		if planes_so >= situation.SOpoints:
			break
		plane = pick_strategy(legal_actions(campaign))
		planes.append(plane())
		"""TODO: implement methods to determine continue pick plane or not """
		to_pick_or_not = determine_strategy([True, False])
	return planes

def random_strategy(possible_choices):
	return random.choice(possible_choices)

class Weapon:
	def __init__(self, weaponPoints, ordnancePoints, attackNumber, attackRange, altitudeAttacks, VB, independence):
		self.weaponPoints = weaponPoints
		self.ordnancePoints = ordnancePoints
		self.attackNumber = attackNumber
		self.attackRange = attackRange
		# A tuple of number interval to specify the range
		self.altitudeAttacks = altitudeAttacks
		# a list specifying which height to attack, in form of [boolean, boolean] correspond to {high, low}
		self.VB = VB
		# Vehicle/building or not, in form of boolean
		self.independence = independence
		# independent or not, boolean
		###for detailed discription see weapon section in rule book
	def attack(self, target, dice_roll):
		if dice_roll >= self.attackNumber:
			return
			# TODO: fill in this method to enable attack
		return

class VB_Weapon(Weapon):
	def __init__(self, weaponPoints, ordnancePoints, attackNumber, attackRange, altitudeAttacks):
		Weapon.__init__(self, weaponPoints, ordnancePoints, attackNumber, attackRange, altitudeAttacks, True, False)
	
	def attack(self, target, dice_roll):
		if dice_roll >= self.attackNumber:
			return
			# TODO: fill in this method to enable attack
		return

class Independent_Weapon(Weapon):
	def __init__(self, weaponPoints, ordnancePoints, attackNumber, attackRange, altitudeAttacks):
		Weapon.__init__(self, weaponPoints, ordnancePoints, attackNumber, attackRange, altitudeAttacks, False, True)

	def attack(self, target, dice_roll):
		if dice_roll >= self.attackNumber:
			return
			# TODO: fill in this method to enable attack
		return

class Ordinary_Weapon(Weapon):
	def __init__(self, weaponPoints, ordnancePoints, attackNumber, attackRange, altitudeAttacks):
		Weapon.__init__(self, weaponPoints, ordnancePoints, attackNumber, attackRange, altitudeAttacks, False, False)

	def attack(self, target, dice_roll):
		if dice_roll >= self.attackNumber:
			return
			# TODO: fill in this method to enable attack
		return

class MK_83(Ordinary_Weapon):
	def __init__(self):
		Weapon.__init__(2, 0, 4, (0, 0), [True, True])

class LAU_61(Ordinary_Weapon):
	def __init__(self):
		Weapon.__init__(2, 1, 4, (0, 1), [True, True])

class AGM_114(VB_Weapon):
	def __init__(self):
		Weapon.__init__(1, 1, 4, (1, 2), [True, True])

class GBU_12(Independent_Weapon):
	def __init__(self):
		Weapon.__init__(1, 1, 4, (0, 1), [True, False])

class AGM_65(VB_Weapon):
	def __init__(self):
		Weapon.__init__(2, 1, 1, (1, 3), [True, True])

class TestMethods(unittest.TestCase):
	def test_legal_actions(self):
		test_campaign = Iraq()
		for plane in legal_actions(test_campaign):
			self.assertTrue(plane().year <= 1991)

	def test_get_all_planes(self):
		test_campaign = Iraq()
		test_situation = Surge()
		sample = get_all_planes(test_campaign, test_situation, random_strategy, random_strategy)
		for plane in sample:
			self.assertTrue(plane.year <= 1991)
		self.assertTrue(sum([p.so for p in sample]) <= 38)

if __name__ == '__main__':
    unittest.main()
