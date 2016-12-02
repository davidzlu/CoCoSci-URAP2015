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

"""battalion information on cards"""
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
        self.units = get_enemy_units([["AAA", 4], ["APC", 8], ["Commands", 2], ["Infantry", 10], ["Truck", 4]])
        self.half_value = 20
        self.destroy_value = 5

class HeadQuarters:
    def __init__(self):
        self.vp = 4
        self.type = (5, "C")
        self.units = get_enemy_units([["AAA", 2], ["AAA Sites", 2], ["APC", 2], ["Buildings", 6],
                                      ["Helicopters", 2], ["Infantry", 2], ["SAM", 2], ["Storage", 2], ["Truck", 2]])
        self.half_value = 29
        self.destroy_value = 7
        """TODO list: special note here"""

class ReconInForce:
    def __init__(self):
        self.vp = 1
        self.type = (4, "C")
        self.units = get_enemy_units([["APC", 4], ["Helicopters", 2], ["Tank", 2], ["Truck", 2]])
        self.half_value = 10
        self.destroy_value = 2
        """TODO list: special note here"""

class ScoutGroup:
    def __init__(self):
        self.vp = 3
        self.type = (2, "C")
        self.units = get_enemy_units([["APC", 2], ["Commands", 2], ["Tank", 2], ["Truck", 2]])
        self.half_value = 10
        self.destroy_value = 2
        """TODO list: special note here"""

class EngineerUnit:
    def __init__(self):
        self.vp = 2
        self.type = (6, "S")
        self.units = get_enemy_units([["APC", 4], ["Infantry", 2], ["Truck", 4]])
        self.half_value = 6
        self.destroy_value = 2
        """TODO list: special note here"""

class FuelDepot:
    def __init__(self):
        self.vp = 4
        self.type = (5, "S")
        self.units = get_enemy_units([["AAA Sites", 2], ["Buildings", 6], ["Infantry", 2], ["Storage", 6], ["Truck", 4]])
        self.half_value = 17
        self.destroy_value = 4
        """TODO list: special note here"""

class SupplyDepot:
    def __init__(self):
        self.vp = 3
        self.type = (4, "S")
        self.units = get_enemy_units([["AAA Sites", 4], ["Buildings", 4], ["Infantry", 4], ["Storage", 4], ["Truck", 6]])
        self.half_value = 23
        self.destroy_value = 6
        """TODO list: special note here"""

class Reserves:
    def __init__(self):
        self.vp = 1
        self.type = (7, "S")
        self.units = get_enemy_units([["APC", 2], ["Infantry", 2], ["SCUD", 2], ["SPA", 2], ["Tank", 2], ["Truck", 2]])
        self.half_value = 12
        self.destroy_value = 3
        """TODO list: special note here"""

class Convoy:
    def __init__(self):
        self.vp = 1
        self.type = (2, "S")
        self.units = get_enemy_units([["APC", 4], ["Truck", 6]])
        self.half_value = 7
        self.destroy_value = 2
        """TODO list: special note here"""

class AirDefenseUnit:
    def __init__(self):
        self.vp = 4
        self.type = (12, "A")
        self.units = get_enemy_units([["AAA", 4], ["APC", 2], ["SAM", 2]])
        self.half_value = 10
        self.destroy_value = 2
        """TODO list: special note here"""

class TankLeader:
    def __init__(self):
        self.vp = 4
        self.type = (11, "A")
        self.units = get_enemy_units([["AAA", 2], ["Commands", 2], ["Helicopters", 2], ["Tank", 4]])
        self.half_value = 16
        self.destroy_value = 4
        """TODO list: special note here"""

class Dismounted:
    def __init__(self):
        self.vp = 2
        self.type = (7, "A")
        self.units = get_enemy_units([["APC", 2], ["Commands", 2], ["Infantry", 6], ["Truck", 2]])
        self.half_value = 11
        self.destroy_value = 3
        """TODO list: special note here"""

class FastAssault:
    def __init__(self):
        self.vp = 3
        self.type = (9, "A")
        self.units = get_enemy_units([["APC", 4], ["Tank", 4], ["Truck", 4]])
        self.half_value = 10
        self.destroy_value = 2
        """TODO list: special note here"""

class Mechanized:
    def __init__(self):
        self.vp = 3
        self.type = (3, "A")
        self.units = get_enemy_units([["AAA", 2], ["APC", 4], ["Infantry", 4], ["Tank", 2]])
        self.half_value = 10
        self.destroy_value = 2

class TankForce:
    def __init__(self):
        self.vp = 5
        self.type = (2, "A")
        self.units = get_enemy_units([["AAA", 2], ["Helicopters", 2], ["SAM", 2], ["Tank", 10]])
        self.half_value = 22
        self.destroy_value = 5

class TankSpearhead:
    def __init__(self):
        self.vp = 6
        self.type = (6, "A")
        self.units = get_enemy_units([["AAA", 2], ["Helicopters", 2], ["SAM", 2], ["Tank", 10]])
        self.half_value = 22
        self.destroy_value = 5
        """TODO list: special note here"""

class ScoutForce:
    def __init__(self):
        self.vp = 2
        self.type = (8, "A")
        self.units = get_enemy_units([["APC", 2], ["Helicopters", 2], ["Tank", 2], ["Truck", 2]])
        self.half_value = 8
        self.destroy_value = 2

class MixedForce:
    def __init__(self):
        self.vp = 3
        self.type = (4, "A")
        self.units = get_enemy_units([["APC", 4], ["Commands", 2], ["Helicopters", 2], ["SPA", 4], ["Tank", 2]])
        self.half_value = 18
        self.destroy_value = 5

class Bombardment:
    def __init__(self):
        self.vp = 4
        self.type = (3, "S")
        self.units = get_enemy_units([["AAA", 4], ["APC", 2], ["SCUD", 6], ["SPA", 4], ["Truck", 2]])
        self.half_value = 23
        self.destroy_value = 6
        """TODO list: special note here"""

class ForwardBase:
    def __init__(self):
        self.vp = 3
        self.type = (6, "C")
        self.units = get_enemy_units([["AAA Sites", 2], ["APC", 2], ["Buildings", 2], ["SCUD", 6], ["Storage", 2]])
        self.half_value = 13
        self.destroy_value = 3
        """TODO list: special note here"""

class MountedInfantry:
    def __init__(self):
        self.vp = 4
        self.type = (5, "A")
        self.units = get_enemy_units([["APC", 8], ["Commands", 2], ["Infantry", 4], ["SAM", 4], ["Truck", 2]])
        self.half_value = 17
        self.destroy_value = 4
        """TODO list: special note here"""

class CommandUnit:
    def __init__(self):
        self.vp = 5
        self.type = (1, "C")
        self.units = get_enemy_units([["APC", 2], ["Commands", 4], ["SAM", 4]])
        self.half_value = 18
        self.destroy_value = 5
        """TODO list: special note here"""

class ArtilleryUnit:
    def __init__(self):
        self.vp = 6
        self.type = (1, "S")
        self.units = get_enemy_units([["Infantry", 4], ["SAM", 2], ["SCUD", 6], ["SPA", 4]])
        self.half_value = 22
        self.destroy_value = 5
        """TODO list: special note here"""

class InfantryFormation:
    def __init__(self):
        self.vp = 2
        self.type = (10, "A")
        self.units = get_enemy_units([["APC", 4], ["Infantry", 6], ["Truck", 4]])
        self.half_value = 17
        self.destroy_value = 4

class SectorMap:
    def __init__(self):
        self.erear = []
        self.etransit = []
        self.frontline = []
        self.ftransit = []
        self.frear = []
        self.airbase = []
        self.scouts = 0
        self.places = [self.erear, self.etransit, self.frontline, self.ftransit, self.frear, self.airbase]
        self.potential_enemies = {}

    def can_put_piece(self, piece, location, constraints=None):
        # if special note, place piece somewhere else
        if piece.type[1] == "A" and location is self.frontline:
            return True
        if piece.type[1] == "S" and location is self.etransit:
            return True
        if piece.type[1] == "C" and location is self.erear:
            return True
        return False

    # def place_piece(self, piece, location, constraints=None):
    #     location.append(piece)

    def place_piece(self, piece, constraints=None):
        for place in self.places:
            if self.can_put_piece(piece, place):
              #  self.place_piece(piece, place)
                self.place.append(piece)

    def place_all_enemy_units(self, list_of_battalions):
        for battalion in list_of_battalions:
            self.place_piece(battalion)

    def setup_enemy_units(self):
        self.potential_enemies = {"C": [MobileHQ(), HeadQuarters(), ReconInForce(), ScoutGroup(), ForwardBase(), \
        CommandUnit()], \
        "A": [InfantryForce(), AirDefenseUnit(), TankLeader(), Dismounted(), FastAssault(), Mechanized(), \
        TankForce(), TankSpearhead(), ScoutForce(), MixedForce(), MountedInfantry(), InfantryFormation()], \
        "S": [EngineerUnit(), FuelDepot(), SupplyDepot(), Reserves(), Convoy(), Bombardment(), ArtilleryUnit()]}

    def get_next_unit(self, list_of_battalions):
        next = None
        if len(list_of_battalions) in range(0, 2):
            next = random.choice(self.potential_enemies["A"])
        elif list_of_battalions[-1].type[1] == "A" and list_of_battalions[-2].type[1] == "A":
            next = random.choice(self.potential_enemies["S"])
        elif list_of_battalions[-1].type[1] == "S":
            next = random.choice(self.potential_enemies["C"])
        elif list_of_battalions[-1].type[1] == "A" and list_of_battalions[-2].type[1] == "C":
            next = random.choice(self.potential_enemies["A"])
        elif list_of_battalions[-1].type[1] == "C" and list_of_battalions[-2].type[1] == "S":
            next = random.choice(self.potential_enemies["A"])
        list_of_battalions.append(next)
        return list_of_battalions

    def get_all_enemies(self, campaign):
        constraint = Constraint()
        battalions = []
        while True:
            battalion_vp = 0
            if battalions != None:
                battalion_vp = sum([b.vp for b in battalions])
            if battalion_vp >= campaign.setup_vp:
                break
            battalions = self.get_next_unit(battalions)
        return battalions

    def place_enemy_units(self, campaign):
        """the method to call for placing all enemy units"""
        battalions = self.get_all_enemies(campaign)
        self.place_all_enemy_units(battalions)



class TestMethods(unittest.TestCase):
    def test_get_enemy_units_mobile_HQ(self):
        self.assertTrue(MobileHQ().units == ["AAA", "AAA", "APC", "APC", "Commands",
                                             "Commands", "Commands", "Commands", "SCUD", "SCUD", "SPA", "SPA", "Truck", "Truck"])
    def test_sector_map(self):
        sm = SectorMap()
        cu = CommandUnit()
        self.assertTrue(sm.can_put_piece(cu, sm.erear))
        sm.place_piece(cu, sm.erear)
        #self.assertTrue(sm.erear == [""])
        #print(sm.erear)

    def test_get_all_enemies(self):
        sm = SectorMap()
        sm.setup_enemy_units()
        campaign = Iraq()
        enemy_list = sm.get_all_enemies(campaign)
        c = Constraint()
        self.assertTrue(c.setup_constraint_battalion_VP(campaign, enemy_list))
        self.assertTrue(c.setup_constraint_batallion_cycle(enemy_list))

if __name__ == '__main__':
    unittest.main()