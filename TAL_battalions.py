import random
from TAL_terrain import *
from TAL_campaigns import *
from TAL_situation import *

def get_enemy_units(list_unittype_num):
	enemy_unit = []
	for element in list_unittype_num:
		for i in range(0, element[1]):
			enemy_unit.append(element[0])
	return enemy_unit

class MobileHQ:
	self.vp = 2
	self.place = (3, "C")
	self.units = get_enemy_units([["AAA", 2], ["APC", 2], ["Commands", 4], ["SCUD", 2], ["SPA", 2], ["Truck", 2]])
	self.half_value = 16
	self.destroy_value = 5

