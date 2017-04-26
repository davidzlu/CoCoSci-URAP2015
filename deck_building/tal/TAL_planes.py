import random
import unittest
from deck_building.tal import TAL_campaigns, TAL_situation

class Plane:
    """Abstract class for planes. Defines instance variables and
    common methods.
    """
    def __init__(self):
        self.year = 0
        self.cannon = 0
        self.so = 0
        self.hit = 0
        self.weapons_equipped = [] # The weapons the agent chose to equip to plane
        self.weapon_set = set() #
        self.weight = 0
        self.special = None
        self.altitude = 1 #1 means high and 0 means low
        self.name = None
        
        self.speed = 1 # 0 for slow, 1 for fast
        self.altitude = 1 # 0 for low, 1 for high
        self.movements = 0 # Total number of hexes the plane can move
        self.cur_moves = 0 # Number of hexes the plane has currently moved
        self.tile = None # The tile plane is currently in
        
    def reset_movement(self):
        self.cur_moves = 0

    def get_year(self):
        return self.year

    def get_cannon(self):
        return self.cannon

    def get_cost(self):
        return self.so

    def get_hitpoints(self):
        return self.hit

    def get_weapons_equip(self):
        return self.weapons_equipped

    def get_weapon_set(self):
        return self.weapon_set

    def get_weight(self):
        return self.weight

    def get_altitude(self):
        return self.altitude

    def get_name(self):
        return self.name
    
    def get_tile(self):
        return self.tile
    
    def get_location(self):
        return self.get_tile(), self.get_tile().get_location(self)
    
    def check_valid_movement(self, start_hex, start_edge, dest_hex, dest_edge):
        if start_hex.get_neighbor(start_edge) == dest_hex:
            if dest_edge != dest_hex.get_opposite_edge(start_edge):
                return True
        return False
    
    def change_altitude(self):
        self.altitude = (self.altitude + 1) % 2
        
    def ridge_evasion(self):
        return

    def move(self, dest_hex, dest_edge):
        """Moves aircraft one step to hex_edge if possible.
        """
        if self.cur_moves < self.movements:
            cur_tile, cur_edge = self.get_location()
            if self.check_valid_movement(cur_tile, cur_edge, dest_hex, dest_edge):
                crossing_ridge = cur_tile.edge_has_ridge(cur_edge) or dest_hex.edge_has_ridge(dest_hex.get_opposite_edge(cur_edge))    
                if not self.altitude and crossing_ridge:
                    result = self.ridge_evasion()
                cur_tile.remove_piece(self)
                dest_hex.add_piece(self, dest_edge)
                self.cur_moves += 1
        else:
            #Go to next plane
            #Reset movement?
            return        

class A_10A(Plane):
    def __init__(self):
        Plane.__init__(self)
        self.year = 1976
        self.cannon = 4
        self.so = 8
        self.hit = 3
        self.weapon_set = {'AIM_9', 'AIM_92', 'MK_20', 'LAU_61', 'LAU_68', 'AGM_114', 'AGM_65', 'MK_82', 'MK_83',
                           'GBU_12', 'GBU_16', 'ECM Pod', 'Fuel Tank'}
        self.weight = 14
        self.name = 'A_10A'

class AH_1(Plane):
    def __init__(self):
        Plane.__init__(self)
        self.year = 1967
        self.cannon = 9
        self.so = 2
        self.hit = 1
        self.weapon_set = {'AIM_9', 'AIM_92', 'BGM_71', 'LAU_61', 'LAU_68', 'AGM_114', 'Fuel Tank'}
        self.weight = 6
        self.name = 'AH_1'

class F_16(Plane):
    def __init__(self):
        Plane.__init__(self)
        self.year = 1976
        self.cannon = 7
        self.so = 5
        self.hit = 2
        self.weapon_set = {'AIM_9', 'MK_20', 'LAU_61', 'LAU_68', 'AGM_65', 'MK_82', 'MK_83', 'GBU_12',
                           'GBU_16', 'ECM Pod', 'Fuel Tank'}
        self.weight = 10
        self.name = 'F_16'

class AH_64A(Plane):
    def __init__(self):
        Plane.__init__(self)
        self.year = 1986
        self.cannon = 7
        self.so = 4
        self.hit = 2
        self.weapon_set = {'AIM_9', 'AIM_92', 'LAU_61', 'LAU_68', 'AGM_114', 'Fuel Tank'}
        self.weight = 8
        self.name = 'AH_64A'

class AV_8B(Plane):
    def __init__(self):
        Plane.__init__(self)
        self.year = 1985
        self.cannon = 7
        self.so = 6
        self.hit = 2
        self.weapon_set = {'AIM_9', 'AIM_92', 'MK_20', 'LAU_61', 'LAU_68', 'AGM_65', 'AGM_114', 'MK_82', 'MK_83', 'GBU_12',
                           'GBU_16', 'ECM Pod', 'Fuel Tank'}
        self.weight = 10
        self.name = 'AV_8B'

class A_10C(Plane):
    def __init__(self):
        Plane.__init__(self)
        self.year = 2006
        self.cannon = 4
        self.so = 9
        self.hit = 3
        self.weapon_set = {'AIM_9', 'AIM_92', 'MK_20', 'LAU_61', 'LAU_68', 'AGM_65', 'AGM_114', 'MK_82', 'MK_83', 'GBU_12',
                           'GBU_16', 'ECM Pod', 'Fuel Tank'}
        self.weight = 14
        self.name = 'A_10C'

class MQ_1(Plane):
    def __init__(self):
        Plane.__init__(self)
        self.year = 2001
        self.cannon = 0
        self.so = 4
        self.hit = 0
        self.weapon_set = {'AGM_114'}
        self.weight = 0
        self.name = 'MQ_1'

class RQ_1(Plane):
    def __init__(self):
        Plane.__init__(self)
        self.year = 1995
        self.cannon = 0
        self.so = 4
        self.hit = 0
        self.weight = 0
        self.name = 'RQ_1'

class AH_64D(Plane):
    def __init__(self):
        Plane.__init__(self)
        self.year = 1997
        self.cannon = 7
        self.so = 5
        self.hit = 2
        self.weapon_set = {'AIM_9', 'AIM_92', 'LAU_61', 'LAU_68', 'AGM_114', 'Fuel Tank'}
        self.weight = 8
        self.name = 'AH_64D'

class AC_130(Plane):
    def __init__(self):
        Plane.__init__(self)
        self.year = 1995
        self.cannon = 5 # or 3 or 1
        self.so = 10
        self.hit = 3
        """TODO: special effect"""
        self.weight = 0
        self.name = 'AC_130'

plane_pool = {A_10A: 4, AH_1: 3, F_16: 1, AH_64A: 8, AV_8B: 3, A_10C: 2, MQ_1: 2, RQ_1: 2, AH_64D: 4, AC_130: 1}

def legal_actions(campaign):
    possible_choices = []
    for plane in plane_pool.keys():
        if plane().year <= campaign.year and plane_pool[plane] > 0:
            possible_choices.append(plane)
    return possible_choices

def get_all_planes(talinst, situation, strategy):
    planes = []
    while True:
        if situation.SOpoints <= 0:
            break
        plane = strategy(talinst) #either returns a plane or False to indicate stop picking
        if plane:
            chosen_plane = plane()
            if chosen_plane.so <= situation.SOpoints:
                if plane_pool[type(chosen_plane)] > 0:
                    planes.append(chosen_plane)
                    situation.SOpoints -= chosen_plane.so
                    plane_pool[type(chosen_plane)] -= 1
        else:
            break
    return planes

class Weapon:
    def __init__(self, weaponWeight, ordnancePoints, attackNumber, attackRange, altitudeAttacks, VB, independence):
        self.weaponWeight = weaponWeight
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
        self.hex = False #whether attack affects entire hex or not
        self.expend = True #whether weapon is expended or retained after an attack
        ###for detailed description see weapon section in rule book
    def attack(self, target, dice_roll):
        if dice_roll >= self.attackNumber:
            target.active = False
        # removing weapon from set will be a separate method

class VB_Weapon(Weapon):
    def __init__(self, weaponWeight, ordnancePoints, attackNumber, attackRange, altitudeAttacks):
        Weapon.__init__(self, weaponWeight, ordnancePoints, attackNumber, attackRange, altitudeAttacks, True, False)

    def attack(self, target, dice_roll):
        if dice_roll >= self.attackNumber:
            return
            # TODO: fill in this method to enable attack
        return

class Independent_Weapon(Weapon):
    def __init__(self, weaponWeight, ordnancePoints, attackNumber, attackRange, altitudeAttacks):
        Weapon.__init__(self, weaponWeight, ordnancePoints, attackNumber, attackRange, altitudeAttacks, False, True)

    def attack(self, target, dice_roll):
        if dice_roll >= self.attackNumber:
            return
            # TODO: fill in this method to enable attack
        return

class Ordinary_Weapon(Weapon):
    def __init__(self, weaponWeight, ordnancePoints, attackNumber, attackRange, altitudeAttacks):
        Weapon.__init__(self, weaponWeight, ordnancePoints, attackNumber, attackRange, altitudeAttacks, False, False)

    def attack(self, target, dice_roll):
        if dice_roll >= self.attackNumber:
            return
            # TODO: fill in this method to enable attack
        return

class MK_20(Ordinary_Weapon):
    def __init__(self):
        Ordinary_Weapon.__init__(self, 1, 1, 6, (0, 0), [True, True])
        self.hex = True

class MK_82(Ordinary_Weapon):
    def __init__(self):
        Ordinary_Weapon.__init__(self, 1, 0, 7, (0, 0), [True, True])

class MK_83(Ordinary_Weapon):
    def __init__(self):
        Ordinary_Weapon.__init__(self, 2, 0, 4, (0, 0), [True, True])

class LAU_61(Ordinary_Weapon):
    def __init__(self):
        Ordinary_Weapon.__init__(self, 2, 1, 4, (0, 1), [True, True])
        self.retain = 7

class LAU_68(Ordinary_Weapon):
    def __init__(self):
        Ordinary_Weapon.__init__(self, 2, 0, 6, (0, 1), [True, True])
        self.retain = 9

class AGM_114(VB_Weapon):
    def __init__(self):
        VB_Weapon.__init__(self, 1, 1, 4, (1, 2), [True, True])

class BGM_71(VB_Weapon):
    def __init__(self):
        VB_Weapon.__init__(self, 1, 0, 7, (1, 1), [True, True])

class GBU_12(Independent_Weapon):
    def __init__(self):
        Independent_Weapon.__init__(self, 1, 1, 4, (0, 1), [True, False])

class GBU_16(Independent_Weapon):
    def __init__(self):
        Independent_Weapon.__init__(self, 2, 1, 0, (0, 1), [True, False])

class AGM_65(VB_Weapon):
    def __init__(self):
        VB_Weapon.__init__(self, 2, 1, 1, (1, 3), [True, True])

class AIM_92(Ordinary_Weapon):
    def __init__(self):
        Ordinary_Weapon.__init__(self, 1, 0, 7, (0, 1), [True, True])

class AIM_9(Ordinary_Weapon):
    def __init__(self):
        Ordinary_Weapon.__init__(self, 1, 1, 3, (0, 3), [True, True])

class FUEL:
    def __init__(self):
        self.weaponWeight = 2
        self.ordnancePoints = 0

class ECM:
    def __init__(self):
        self.weaponWeight = 1
        self.ordnancePoints = 1

weapon_pool = {MK_20: 16, LAU_61: 16, MK_83: 8, GBU_16: 8, AGM_65: 16, AGM_114: 16, LAU_68: 6, BGM_71: 6,
               GBU_12: 8, MK_82: 8, AIM_9: 4, AIM_92: 4, FUEL: 4, ECM: 4}

def get_weapon(weapon_name):
    if weapon_name == 'MK_20':
        return MK_20()
    elif weapon_name == 'LAU_61':
        return LAU_61()
    elif weapon_name == 'MK_83':
        return MK_83()
    elif weapon_name == 'GBU_16':
        return GBU_16()
    elif weapon_name == 'AGM_65':
        return AGM_65()
    elif weapon_name == 'AGM_114':
        return AGM_114()
    elif weapon_name == 'LAU_68':
        return LAU_68()
    elif weapon_name == 'BGM_71':
        return BGM_71()
    elif weapon_name == 'GBU_12':
        return GBU_12()
    elif weapon_name == 'MK_82':
        return MK_82()
    elif weapon_name == 'AIM_9':
        return AIM_9()
    elif weapon_name == 'AIM_92':
        return AIM_92()
    elif weapon_name == 'FUEL':
        return FUEL()
    elif weapon_name == 'ECM':
        return ECM()

def arm_aircraft(talinst, planes, policy):
    #implement weight point penalty of range band + fueling priority
    policy(talinst)

class TestMethods(unittest.TestCase):
    def test_legal_actions(self):
        test_campaign = TAL_campaigns.Iraq()
        for plane in legal_actions(test_campaign):
            self.assertTrue(plane().year <= 1991)

    # def test_get_all_planes(self):
    #     test_campaign = TAL_campaigns.Iraq()
    #     test_situation = TAL_situation.Surge()
    #     sample = get_all_planes(test_campaign, test_situation, random_policy)
    #     for plane in sample:
    #         self.assertTrue(plane.year <= 1991)
    #     self.assertTrue(sum([p.so for p in sample]) <= 38)

if __name__ == '__main__':
    unittest.main()
