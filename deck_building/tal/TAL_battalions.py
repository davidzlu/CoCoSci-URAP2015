import random
import unittest
from deck_building.tal.TAL_campaigns import *
from enum import Enum
"""Enums are a way of defining a set of constant names in a way
more organized than a bunch of global variables. See 
https://docs.python.org/3/library/enum.html for details on enums
"""

class BattalionNames(Enum):
    MOBILEHQ = "mobile hq"
    INFANTRYFORCE = "infantry force"
    HEADQUARTERS = "headquarters"
    REACONINFORCE = "recon in force"
    SCOUTGROUP = "scout group"
    ENGINEERUNIT = "engineer unit"
    FUELDEPOT = "fuel depot"
    SUPPLYDEPOT = "supply depot"
    RESERVES = "reserves"
    CONVOY = "convoy"
    AIRDEFENSEUNIT = "air defense unit"
    TANKLEADER = "tank leader"
    DISMOUNTED = "dismounted"
    FASTASSAULT = "fast assault"
    MECHANIZED = "mechanized"
    TANKFORCE = "tank force"
    TANKSPEARHEAD = "tank spearhead"
    SCOUTFORCE = "scout force"
    MIXEDFORCE = "mixed force"
    BOMBARDMENT = "bombardment"
    FORWARDBASE = "forward base"
    MOUNTEDINFANTRY = "mounted infantry"
    COMMANDUNIT = "command unit"
    ARTILLERYUNIT = "artillery unit"
    INFANTRYFORMATION = "infantry formation"

class EnemyUnitNames(Enum):
    """Enum of enemy unit names
    """
    AAA = "aaa"
    AAA_SITE = "aaa site"
    APC = "apc"
    BUILDING = "building"
    COMMAND = "command"
    HELICOPTER = "helicopter"
    INFANTRY = "infantry"
    SAM = "sam"
    SCUD = "scud"
    SPA = "spa"
    STORAGE = "storage"
    TANK = "tank"
    TRUCK = "truck"

class EnemyAttackTypes(Enum):
    HEAVY = "heavy"
    LIGHT = "light"

class EnemyUnitTypes(Enum):
    V = "v"
    B = "b"

def get_enemy_units(list_unittype_num):
    """Returns a list of enemy unit objects.
    
    Parameters:
     - list_unittype_num: a list of [Enemy unit constructor, # instances] lists
     """
    enemy_unit = []
    for element in list_unittype_num:
        for i in range(0, element[1]):
            enemy_unit.append(element[0]())
            assert(type(enemy_unit[-1]) == EnemyUnit)
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
        self.map_location = ""
        self.name = ""
        self.special = self.special_effect() #Field for special instructions for this battalion
        
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return self.name == other.name
        
    def get_location(self):
        a = "front line"
        s = "enemy transit"
        c = "enemy rear"
        typ = self.type[1]
        if typ == "A":
            return a
        elif typ == "S":
            return s
        elif typ == "C":
            return c 
        
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
        
class EnemyUnit:
    """Abstract class for enemy units. See page 11 of game manual
    for details on each field.
    """
        
    def __init__(self):
        self.point_value = 0
        self.attack_type = None
        self.attack_number = 0
        self.attack_range = 0
        self.unit_type = None
        self.unit_name = None
        self.roll_modifier = 0
        self.active = True

    def get_point_value(self):
        return self.point_value

    def get_attack_type(self):
        return self.attack_type

    def get_attack_number(self):
        return self.attack_number

    def get_attack_range(self):
        return self.attack_range

    def get_unit_type(self):
        return self.unit_type

    def get_unit_name(self):
        return self.unit_name

    def get_roll_modifier(self):
        return self.roll_modifier
    
    def is_active(self):
        return self.active
    
class AAA(EnemyUnit):
    
    def __init__(self):
        self.point_value = 2
        self.attack_type = EnemyAttackTypes.HEAVY
        self.attack_number = 2
        self.attack_range = 1
        self.unit_type = EnemyUnitTypes.V
        self.unit_name = EnemyUnitNames.AAA
        self.roll_modifier = 0
        
class AAASite(EnemyUnit):
    
    def __init__(self):
        self.point_value = 2
        self.attack_type = EnemyAttackTypes.LIGHT
        self.attack_number = 3
        self.attack_range = 2
        self.unit_type = EnemyUnitTypes.B
        self.unit_name = EnemyUnitNames.AAA_SITE
        self.roll_modifier = 0
        
class APC(EnemyUnit):
    
    def __init__(self):
        self.point_value = 1
        self.attack_type = EnemyAttackTypes.LIGHT
        self.attack_number = 1
        self.attack_range = 0
        self.unit_type = EnemyUnitTypes.V
        self.unit_name = EnemyUnitNames.APC
        self.roll_modifier = 0
        
class Building(EnemyUnit):
    
    def __init__(self):
        self.point_value = 3
        self.attack_type = EnemyAttackTypes.LIGHT
        self.attack_number = 1
        self.attack_range = 0
        self.unit_type = EnemyUnitTypes.B
        self.unit_name = EnemyUnitNames.BUILDING
        self.roll_modifier = -4
        
class Command(EnemyUnit):
    
    def __init__(self):
        self.point_value = 4
        self.attack_type = EnemyAttackTypes.LIGHT
        self.attack_number = 2
        self.attack_range = 1
        self.unit_type = EnemyUnitTypes.V
        self.unit_name = EnemyUnitNames.COMMAND
        self.roll_modifier = 0
        
class Helicopter(EnemyUnit):
    
    def __init__(self):
        self.point_value = 3
        self.attack_type = EnemyAttackTypes.HEAVY
        self.attack_number = 2
        self.attack_range = 1
        self.unit_type = None
        self.unit_name = EnemyUnitNames.HELICOPTER
        self.roll_modifier = 0
        self.speed = 1
        
    def get_speed(self):
        return self.speed
    
class Infantry(EnemyUnit):
    
    def __init__(self):
        self.point_value = 1
        self.attack_type = EnemyAttackTypes.LIGHT
        self.attack_number = 1
        self.attack_range = 1
        self.unit_type = None
        self.unit_name = EnemyUnitNames.INFANTRY
        self.roll_modifier = 0
        
class SAM(EnemyUnit):
    
    def __init__(self):
        self.point_value = 3
        self.attack_type = EnemyAttackTypes.HEAVY
        self.attack_number = 2
        self.attack_range = 3
        self.unit_type = EnemyAttackTypes.V
        self.unit_name = EnemyUnitNames.SAM
        self.roll_modifier = 0
    
class SCUD(EnemyUnit):
    
    def __init__(self):
        self.point_value = 3
        self.attack_type = None
        self.attack_number = None
        self.attack_range = 0
        self.unit_type = EnemyAttackTypes.V
        self.unit_name = EnemyUnitNames.SCUD
        self.roll_modifier = 0
        
class SPA(EnemyUnit):
    
    def __init__(self):
        self.point_value = 2
        self.attack_type = None
        self.attack_number = None
        self.attack_range = 0
        self.unit_type = EnemyAttackTypes.V
        self.unit_name = EnemyUnitNames.SPA
        self.roll_modifier = 0
        
class Storage(EnemyUnit):
    
    def __init__(self):
        self.point_value = 2
        self.attack_type = EnemyAttackTypes.LIGHT
        self.attack_number = 1
        self.attack_range = 0
        self.unit_type = EnemyAttackTypes.B
        self.unit_name = EnemyUnitNames.STORAGE
        self.roll_modifier = 0
        
class Tank(EnemyUnit):
    
    def __init__(self):
        self.point_value = 2
        self.attack_type = EnemyAttackTypes.LIGHT
        self.attack_number = 1
        self.attack_range = 0
        self.unit_type = EnemyAttackTypes.V
        self.unit_name = EnemyUnitNames.TANK
        self.roll_modifier = -2
        
class Truck(EnemyUnit):
    
    def __init__(self):
        self.point_value = 1
        self.attack_type = EnemyAttackTypes.LIGHT
        self.attack_number = 1
        self.attack_range = 0
        self.unit_type = EnemyAttackTypes.V
        self.unit_name = EnemyUnitNames.TRUCK
        self.roll_modifier = 2

"""battalion information on cards"""
class MobileHQ(Battalion):
    def __init__(self):
        self.vp = 2
        self.type = (3, "C")
        self.units = get_enemy_units([[AAA, 2], [APC, 2], [Command, 4], [SCUD, 2], [SPA, 2], [Truck, 2]])
        self.half_value = 16
        self.destroy_value = 5
        self.map_location = self.get_location()
        self.name = BattalionNames.MOBILEHQ
        """TODO list: special note here"""

class InfantryForce(Battalion):
    def __init__(self):
        self.vp = 5
        self.type = (1, "A")
        self.units = get_enemy_units([[AAA, 4], [APC, 8], [Command, 2], [Infantry, 10], [Truck, 4]])
        self.half_value = 20
        self.destroy_value = 5
        self.map_location = self.get_location()
        self.name = BattalionNames.INFANTRYFORCE

class HeadQuarters(Battalion):
    def __init__(self):
        self.vp = 4
        self.type = (5, "C")
        self.units = get_enemy_units([[AAA, 2], [AAASite, 2], [APC, 2], [Building, 6],
                                      [Helicopter, 2], [Infantry, 2], [SAM, 2], [Storage, 2], [Truck, 2]])
        self.half_value = 29
        self.destroy_value = 7
        self.map_location = self.get_location()
        self.name = BattalionNames.HEADQUARTERS
        """TODO list: special note here"""

class ReconInForce(Battalion):
    def __init__(self):
        self.vp = 1
        self.type = (4, "C")
        self.units = get_enemy_units([[APC, 4], [Helicopter, 2], [Tank, 2], [Truck, 2]])
        self.half_value = 10
        self.destroy_value = 2
        self.map_location = self.get_location()
        self.name = BattalionNames.RECONINFORCE
        """TODO list: special note here"""

class ScoutGroup(Battalion):
    def __init__(self):
        self.vp = 3
        self.type = (2, "C")
        self.units = get_enemy_units([[APC, 2], [Command, 2], [Tank, 2], [Truck, 2]])
        self.half_value = 10
        self.destroy_value = 2
        self.map_location = self.get_location()
        self.name = BattalionNames.SCOUTGROUP
        """TODO list: special note here"""

class EngineerUnit(Battalion):
    def __init__(self):
        self.vp = 2
        self.type = (6, "S")
        self.units = get_enemy_units([[APC, 4], [Infantry, 2], [Truck, 4]])
        self.half_value = 6
        self.destroy_value = 2
        self.map_location = self.get_location()
        self.name = BattalionNames.ENGINEERUNIT
        """TODO list: special note here"""

class FuelDepot(Battalion):
    def __init__(self):
        self.vp = 4
        self.type = (5, "S")
        self.units = get_enemy_units([[AAASite, 2], [Building, 6], [Infantry, 2], [Storage, 6], [Truck, 4]])
        self.half_value = 17
        self.destroy_value = 4
        self.map_location = self.get_location()
        self.name = BattalionNames.FUELDEPOT
        """TODO list: special note here"""

class SupplyDepot(Battalion):
    def __init__(self):
        self.vp = 3
        self.type = (4, "S")
        self.units = get_enemy_units([[AAASite, 4], [Building, 4], [Infantry, 4], [Storage, 4], [Truck, 6]])
        self.half_value = 23
        self.destroy_value = 6
        self.map_location = self.get_location()
        self.name = BattalionNames.SUPPLYDEPOT
        """TODO list: special note here"""

class Reserves(Battalion):
    def __init__(self):
        self.vp = 1
        self.type = (7, "S")
        self.units = get_enemy_units([[APC, 2], [Infantry, 2], [SCUD, 2], [SPA, 2], [Tank, 2], [Truck, 2]])
        self.half_value = 12
        self.destroy_value = 3
        self.map_location = self.get_location()
        self.name = BattalionNames.RESERVES
        """TODO list: special note here"""

class Convoy(Battalion):
    def __init__(self):
        self.vp = 1
        self.type = (2, "S")
        self.units = get_enemy_units([[APC, 4], [Truck, 6]])
        self.half_value = 7
        self.destroy_value = 2
        self.map_location = self.get_location()
        self.name = BattalionNames.CONVOY
        """TODO list: special note here"""

class AirDefenseUnit(Battalion):
    def __init__(self):
        self.vp = 4
        self.type = (12, "A")
        self.units = get_enemy_units([[AAA, 4], [APC, 2], [SAM, 2]])
        self.half_value = 10
        self.destroy_value = 2
        self.map_location = self.get_location()
        self.name = BattalionNames.AIRDEFENSEUNIT
        """TODO list: special note here"""

class TankLeader(Battalion):
    def __init__(self):
        self.vp = 4
        self.type = (11, "A")
        self.units = get_enemy_units([[AAA, 2], [Command, 2], [Helicopter, 2], [Tank, 4]])
        self.half_value = 16
        self.destroy_value = 4
        self.map_location = self.get_location()
        self.name = BattalionNames.TANKLEADER
        """TODO list: special note here"""

class Dismounted(Battalion):
    def __init__(self):
        self.vp = 2
        self.type = (7, "A")
        self.units = get_enemy_units([[APC, 2], [Command, 2], [Infantry, 6], [Truck, 2]])
        self.half_value = 11
        self.destroy_value = 3
        self.map_location = self.get_location()
        self.name = BattalionNames.DISMOUNTED
        """TODO list: special note here"""

class FastAssault(Battalion):
    def __init__(self):
        self.vp = 3
        self.type = (9, "A")
        self.units = get_enemy_units([[APC, 4], [Tank, 4], [Truck, 4]])
        self.half_value = 10
        self.destroy_value = 2
        self.map_location = self.get_location()
        self.name = BattalionNames.FASTASSAULT
        """TODO list: special note here"""

class Mechanized(Battalion):
    def __init__(self):
        self.vp = 3
        self.type = (3, "A")
        self.units = get_enemy_units([[AAA, 2], [APC, 4], [Infantry, 4], [Tank, 2]])
        self.half_value = 10
        self.destroy_value = 2
        self.map_location = self.get_location()
        self.name = BattalionNames.MECHANIZED

class TankForce(Battalion):
    def __init__(self):
        self.vp = 5
        self.type = (2, "A")
        self.units = get_enemy_units([[AAA, 2], [Helicopter, 2], [SAM, 2], [Tank, 10]])
        self.half_value = 22
        self.destroy_value = 5
        self.map_location = self.get_location()
        self.name = BattalionNames.TANKFORCE

class TankSpearhead(Battalion):
    def __init__(self):
        self.vp = 6
        self.type = (6, "A")
        self.units = get_enemy_units([[AAA, 2], [Helicopter, 2], [SAM, 2], [Tank, 10]])
        self.half_value = 22
        self.destroy_value = 5
        self.map_location = self.get_location()
        self.name = BattalionNames.TANKSPEARHEAD
        """TODO list: special note here"""

class ScoutForce(Battalion):
    def __init__(self):
        self.vp = 2
        self.type = (8, "A")
        self.units = get_enemy_units([[APC, 2], [Helicopter, 2], [Tank, 2], [Truck, 2]])
        self.half_value = 8
        self.destroy_value = 2
        self.map_location = self.get_location()
        self.name = BattalionNames.SCOUTFORCE

class MixedForce(Battalion):
    def __init__(self):
        self.vp = 3
        self.type = (4, "A")
        self.units = get_enemy_units([[APC, 4], [Command, 2], [Helicopter, 2], [SPA, 4], [Tank, 2]])
        self.half_value = 18
        self.destroy_value = 5
        self.map_location = self.get_location()
        self.name = BattalionNames.MIXEDFORCE

class Bombardment(Battalion):
    def __init__(self):
        self.vp = 4
        self.type = (3, "S")
        self.units = get_enemy_units([[AAA, 4], [APC, 2], [SCUD, 6], [SPA, 4], [Truck, 2]])
        self.half_value = 23
        self.destroy_value = 6
        self.map_location = self.get_location()
        self.name = BattalionNames.BOMBARDMENT
        """TODO list: special note here"""

class ForwardBase(Battalion):
    def __init__(self):
        self.vp = 3
        self.type = (6, "C")
        self.units = get_enemy_units([[AAASite, 2], [APC, 2], [Building, 2], [SCUD, 6], [Storage, 2]])
        self.half_value = 13
        self.destroy_value = 3
        self.map_location = self.get_location()
        self.name = BattalionNames.FORWARDBASE
        """TODO list: special note here"""

class MountedInfantry(Battalion):
    def __init__(self):
        self.vp = 4
        self.type = (5, "A")
        self.units = get_enemy_units([[APC, 8], [Command, 2], [Infantry, 4], [SAM, 4], [Truck, 2]])
        self.half_value = 17
        self.destroy_value = 4
        self.map_location = self.get_location()
        self.name = BattalionNames.MOUNTEDINFANTRY
        """TODO list: special note here"""

class CommandUnit(Battalion):
    def __init__(self):
        self.vp = 5
        self.type = (1, "C")
        self.units = get_enemy_units([[APC, 2], [Command, 4], [SAM, 4]])
        self.half_value = 18
        self.destroy_value = 5
        self.map_location = self.get_location()
        self.name = BattalionNames.COMMANDUNIT
        """TODO list: special note here"""

class ArtilleryUnit(Battalion):
    def __init__(self):
        self.vp = 6
        self.type = (1, "S")
        self.units = get_enemy_units([[Infantry, 4], [SAM, 2], [SCUD, 6], [SPA, 4]])
        self.half_value = 22
        self.destroy_value = 5
        self.map_location = self.get_location()
        self.name = BattalionNames.ARTILLERYUNIT
        """TODO list: special note here"""

class InfantryFormation(Battalion):
    def __init__(self):
        self.vp = 2
        self.type = (10, "A")
        self.units = get_enemy_units([[APC, 4], [Infantry, 6], [Truck, 4]])
        self.half_value = 17
        self.destroy_value = 4
        self.map_location = self.get_location()
        self.name = BattalionNames.INFANTRYFORMATION

class SectorMap:
    def __init__(self, setup_vp):
        self.erear = []
        self.etransit = []
        self.frontline = []
        self.ftransit = []
        self.frear = []
        self.airbase = []
        self.scouts = 0
        self.places = [self.erear, self.etransit, self.frontline, self.ftransit, self.frear, self.airbase]
        self.potential_enemies = {}
        self.total_vp = self.setup_enemy_units(setup_vp)

    def can_put_piece(self, piece, location, constraints=None):
        # TODO: Finish writing method once special notes are implemented
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

    def place_piece(self, piece, constraints=None):
        # Each 'place' refers to an area on the sector map, represented as a list
        for place in self.places:
            if self.can_put_piece(piece, place):
                place.append(piece)
                
    def place_all_enemy_units(self, list_of_battalions):
        for battalion in list_of_battalions:
            self.place_piece(battalion)

    def setup_enemy_units(self, setup_vp):
        """Sets up battalion decks and draws to populate sector map. Returns drawn victory points.
        
        Parameters:
         - setup_vp: how many victory points needed before drawing stops
        """
        c_deck =  [MobileHQ(), HeadQuarters(), ReconInForce(), ScoutGroup(), ForwardBase(), CommandUnit()]
        random.shuffle(c_deck)
        a_deck = [InfantryForce(), AirDefenseUnit(), TankLeader(), Dismounted(), FastAssault(), Mechanized(), \
                  TankForce(), TankSpearhead(), ScoutForce(), MixedForce(), MountedInfantry(), InfantryFormation()]
        random.shuffle(a_deck) 
        s_deck = [EngineerUnit(), FuelDepot(), SupplyDepot(), Reserves(), Convoy(), Bombardment(), ArtilleryUnit()]
        random.shuffle(s_deck)
        
        self.potential_enemies = {"C": c_deck,
                                  "A": a_deck,
                                  "S": s_deck}
        drawn_vp = 0
        draw_order = ("A", "A", "S", "C")
        draw_phase = 0
        while drawn_vp < setup_vp:
            deck_to_draw = draw_order[draw_phase]
            batt = self.potential_enemies[deck_to_draw].pop()
            assert(type(batt) == Battalion)
            drawn_vp += batt.get_vp()
            self.place_piece(batt)
            draw_phase = (draw_phase + 1) % len(draw_order)
        return drawn_vp

class TestMethods(unittest.TestCase):
    def test_get_enemy_units_mobile_HQ(self):
        self.assertTrue(MobileHQ().units == [AAA, AAA, APC, APC, Command,
                                             Command, Command, Command, SCUD, SCUD, SPA, SPA, Truck, Truck])
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