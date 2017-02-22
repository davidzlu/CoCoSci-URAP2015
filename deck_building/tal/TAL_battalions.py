import random
import unittest
from deck_building.tal.TAL_campaigns import *

def get_enemy_units(list_unittype_num):
    """construct a list of enemy units in battalion using a list of [unit type, nums of units] sublists"""
    enemy_unit = []
    for element in list_unittype_num:
        for i in range(0, element[1]):
            enemy_unit.append(element[0])
    return enemy_unit

class Battalion:
    """Abstract class for battalions.
    """
    def __init__(self):
        self.vp = 0
        self.type = ()
        self.units = []
        self.half_value = 0
        self.destroy_value = 0
        self.special = self.special_effect #Field for special instructions for this battalion
        
    def get_vp(self):
        return self.vp
    
    def get_type(self):
        return self.type
    
    def get_units(self):
        return self.units
    
    def get_half_value(self):
        return self.half_value
    
    def get_destroy_value(self):
        return self.destroy_value
    
    def get_special(self):
        return self.special
    
    def special_effect(self):
        """Function that performs battalion's special effect
        """
        raise NotImplementedError
        

"""battalion information on cards"""
class MobileHQ(Battalion):
    def __init__(self):
        self.vp = 2
        self.type = (3, "C")
        self.units = get_enemy_units([["AAA", 2], ["APC", 2], ["Commands", 4], ["SCUD", 2], ["SPA", 2], ["Truck", 2]])
        self.half_value = 16
        self.destroy_value = 5
        """TODO list: special note here"""

class InfantryForce(Battalion):
    def __init__(self):
        self.vp = 5
        self.type = (1, "A")
        self.units = get_enemy_units([["AAA", 4], ["APC", 8], ["Commands", 2], ["Infantry", 10], ["Truck", 4]])
        self.half_value = 20
        self.destroy_value = 5

class HeadQuarters(Battalion):
    def __init__(self):
        self.vp = 4
        self.type = (5, "C")
        self.units = get_enemy_units([["AAA", 2], ["AAA Sites", 2], ["APC", 2], ["Buildings", 6],
                                      ["Helicopters", 2], ["Infantry", 2], ["SAM", 2], ["Storage", 2], ["Truck", 2]])
        self.half_value = 29
        self.destroy_value = 7
        """TODO list: special note here"""

class ReconInForce(Battalion):
    def __init__(self):
        self.vp = 1
        self.type = (4, "C")
        self.units = get_enemy_units([["APC", 4], ["Helicopters", 2], ["Tank", 2], ["Truck", 2]])
        self.half_value = 10
        self.destroy_value = 2
        """TODO list: special note here"""

class ScoutGroup(Battalion):
    def __init__(self):
        self.vp = 3
        self.type = (2, "C")
        self.units = get_enemy_units([["APC", 2], ["Commands", 2], ["Tank", 2], ["Truck", 2]])
        self.half_value = 10
        self.destroy_value = 2
        """TODO list: special note here"""

class EngineerUnit(Battalion):
    def __init__(self):
        self.vp = 2
        self.type = (6, "S")
        self.units = get_enemy_units([["APC", 4], ["Infantry", 2], ["Truck", 4]])
        self.half_value = 6
        self.destroy_value = 2
        """TODO list: special note here"""

class FuelDepot(Battalion):
    def __init__(self):
        self.vp = 4
        self.type = (5, "S")
        self.units = get_enemy_units([["AAA Sites", 2], ["Buildings", 6], ["Infantry", 2], ["Storage", 6], ["Truck", 4]])
        self.half_value = 17
        self.destroy_value = 4
        """TODO list: special note here"""

class SupplyDepot(Battalion):
    def __init__(self):
        self.vp = 3
        self.type = (4, "S")
        self.units = get_enemy_units([["AAA Sites", 4], ["Buildings", 4], ["Infantry", 4], ["Storage", 4], ["Truck", 6]])
        self.half_value = 23
        self.destroy_value = 6
        """TODO list: special note here"""

class Reserves(Battalion):
    def __init__(self):
        self.vp = 1
        self.type = (7, "S")
        self.units = get_enemy_units([["APC", 2], ["Infantry", 2], ["SCUD", 2], ["SPA", 2], ["Tank", 2], ["Truck", 2]])
        self.half_value = 12
        self.destroy_value = 3
        """TODO list: special note here"""

class Convoy(Battalion):
    def __init__(self):
        self.vp = 1
        self.type = (2, "S")
        self.units = get_enemy_units([["APC", 4], ["Truck", 6]])
        self.half_value = 7
        self.destroy_value = 2
        """TODO list: special note here"""

class AirDefenseUnit(Battalion):
    def __init__(self):
        self.vp = 4
        self.type = (12, "A")
        self.units = get_enemy_units([["AAA", 4], ["APC", 2], ["SAM", 2]])
        self.half_value = 10
        self.destroy_value = 2
        """TODO list: special note here"""

class TankLeader(Battalion):
    def __init__(self):
        self.vp = 4
        self.type = (11, "A")
        self.units = get_enemy_units([["AAA", 2], ["Commands", 2], ["Helicopters", 2], ["Tank", 4]])
        self.half_value = 16
        self.destroy_value = 4
        """TODO list: special note here"""

class Dismounted(Battalion):
    def __init__(self):
        self.vp = 2
        self.type = (7, "A")
        self.units = get_enemy_units([["APC", 2], ["Commands", 2], ["Infantry", 6], ["Truck", 2]])
        self.half_value = 11
        self.destroy_value = 3
        """TODO list: special note here"""

class FastAssault(Battalion):
    def __init__(self):
        self.vp = 3
        self.type = (9, "A")
        self.units = get_enemy_units([["APC", 4], ["Tank", 4], ["Truck", 4]])
        self.half_value = 10
        self.destroy_value = 2
        """TODO list: special note here"""

class Mechanized(Battalion):
    def __init__(self):
        self.vp = 3
        self.type = (3, "A")
        self.units = get_enemy_units([["AAA", 2], ["APC", 4], ["Infantry", 4], ["Tank", 2]])
        self.half_value = 10
        self.destroy_value = 2

class TankForce(Battalion):
    def __init__(self):
        self.vp = 5
        self.type = (2, "A")
        self.units = get_enemy_units([["AAA", 2], ["Helicopters", 2], ["SAM", 2], ["Tank", 10]])
        self.half_value = 22
        self.destroy_value = 5

class TankSpearhead(Battalion):
    def __init__(self):
        self.vp = 6
        self.type = (6, "A")
        self.units = get_enemy_units([["AAA", 2], ["Helicopters", 2], ["SAM", 2], ["Tank", 10]])
        self.half_value = 22
        self.destroy_value = 5
        """TODO list: special note here"""

class ScoutForce(Battalion):
    def __init__(self):
        self.vp = 2
        self.type = (8, "A")
        self.units = get_enemy_units([["APC", 2], ["Helicopters", 2], ["Tank", 2], ["Truck", 2]])
        self.half_value = 8
        self.destroy_value = 2

class MixedForce(Battalion):
    def __init__(self):
        self.vp = 3
        self.type = (4, "A")
        self.units = get_enemy_units([["APC", 4], ["Commands", 2], ["Helicopters", 2], ["SPA", 4], ["Tank", 2]])
        self.half_value = 18
        self.destroy_value = 5

class Bombardment(Battalion):
    def __init__(self):
        self.vp = 4
        self.type = (3, "S")
        self.units = get_enemy_units([["AAA", 4], ["APC", 2], ["SCUD", 6], ["SPA", 4], ["Truck", 2]])
        self.half_value = 23
        self.destroy_value = 6
        """TODO list: special note here"""

class ForwardBase(Battalion):
    def __init__(self):
        self.vp = 3
        self.type = (6, "C")
        self.units = get_enemy_units([["AAA Sites", 2], ["APC", 2], ["Buildings", 2], ["SCUD", 6], ["Storage", 2]])
        self.half_value = 13
        self.destroy_value = 3
        """TODO list: special note here"""

class MountedInfantry(Battalion):
    def __init__(self):
        self.vp = 4
        self.type = (5, "A")
        self.units = get_enemy_units([["APC", 8], ["Commands", 2], ["Infantry", 4], ["SAM", 4], ["Truck", 2]])
        self.half_value = 17
        self.destroy_value = 4
        """TODO list: special note here"""

class CommandUnit(Battalion):
    def __init__(self):
        self.vp = 5
        self.type = (1, "C")
        self.units = get_enemy_units([["APC", 2], ["Commands", 4], ["SAM", 4]])
        self.half_value = 18
        self.destroy_value = 5
        """TODO list: special note here"""

class ArtilleryUnit(Battalion):
    def __init__(self):
        self.vp = 6
        self.type = (1, "S")
        self.units = get_enemy_units([["Infantry", 4], ["SAM", 2], ["SCUD", 6], ["SPA", 4]])
        self.half_value = 22
        self.destroy_value = 5
        """TODO list: special note here"""

class InfantryFormation(Battalion):
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
        self.setup_enemy_units()

    def can_put_piece(self, piece, location, constraints=None):
        # if special note, place piece somewhere else
        if piece.type[1] == "A" and location is self.frontline:
            return True
        if piece.type[1] == "S" and location is self.etransit:
            return True
        if piece.type[1] == "C" and location is self.erear:
            return True
        return False
    
    def get_battalions_on_map(self):
        return [batt for sector in self.places for batt in sector]

    # def place_piece(self, piece, location, constraints=None):
    #     location.append(piece)

    def place_piece(self, piece, constraints=None):
        #TODO: FINISH WRITING
        for place in self.places:
            if self.can_put_piece(piece, place):
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
        next_unit = None
        if len(list_of_battalions) in range(0, 2):
            next_unit = random.choice(self.potential_enemies["A"])
        elif list_of_battalions[-1].type[1] == "A" and list_of_battalions[-2].type[1] == "A":
            next_unit = random.choice(self.potential_enemies["S"])
        elif list_of_battalions[-1].type[1] == "S":
            next_unit = random.choice(self.potential_enemies["C"])
        elif list_of_battalions[-1].type[1] == "A" and list_of_battalions[-2].type[1] == "C":
            next_unit = random.choice(self.potential_enemies["A"])
        elif list_of_battalions[-1].type[1] == "C" and list_of_battalions[-2].type[1] == "S":
            next_unit = random.choice(self.potential_enemies["A"])
        list_of_battalions.append(next_unit)
        return list_of_battalions

    def get_all_enemies(self, campaign):
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