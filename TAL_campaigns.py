# A Thunderbolt Apache Leader game file to interface with DeckBuilding.py
import random
from TAL_terrain import *
from TAL_battalions import *
from TAL_situation import *
import unittest

def create_board(Campaign):
    piecenums = random.shuffle(Campaign.terrain_nums)
    pieces = []
    for piece in piecenums:
        pieces.append(get_piece(piece)) #get piece will be found in the terrain file
    board = [list(pieces[0:3]), list(pieces[3:7]), list(pieces[7:])]
    return board



class Iraq:
    """Campaign information for Iraq"""
    # Special Note: Do not roll for Battalion Movement on the 1st Day

    def __init__(self):
        self.year = 1991
        self.setup_vp = 26
        self.terrain_nums = [1, 3, 4, 7, 9, 11, 12, 13, 14, 18]
        # Eval has ranges for Dismal, Poor, Adequate, Good, Great
        # Hypothetical upper bound was set on Great
        self.eval = [(0, 6), (7, 9), (10, 12), (13, 19), (20, 100)]


class Libya84:
    # Special Note: Remove 2 "No Enemy" Pop-Ups

    def __init__(self):
        self.year = 1984
        self.setup_vp = 33
        self.terrain_nums = [2, 3, 5, 6, 8, 10, 12, 14, 15, 17]
        # Eval has ranges for Dismal, Poor, Adequate, Good, Great
        # Hypothetical upper bound was set on Great
        self.eval = [(0, 10), (11, 13), (14, 17), (18, 25), (26, 100)]


class Libya11:
    #double check numbers with card
    def __init__(self):
        self.year = 2011
        self.setup_vp = 31
        self.terrain_nums = [1, 3, 5, 6, 8, 10, 12, 14, 15, 17]
        # Eval has ranges for Dismal, Poor, Adequate, Good, Great
        # Hypothetical upper bound was set on Great
        self.eval = [(0, 6), (7, 9), (10, 12), (13, 19), (20, 100)]

class Constrait:
    """a class that stores constrait/rules of the game"""
    def setup_constrait_battalion_VP(self, campaign, battalion):
        """check if the battalion cards that are selected fulfills that
            1. total VP >= setup_vp
            2. after exceeds setup_vp stops drawing
            takes in campaign and a list of battalion being drawn in first to last ORDER"""
        sum_vp = 0
        while len(battalion):
            sum_vp += battalion.pop().vp
            if sum_vp >= campaign.setup_vp:
                if not len(battalion):
                    return True
                else:
                    return False
        return False

class TestMethods(unittest.TestCase):
    def test_setup_constrait_battalion_VP(self):
        # case 1: total battalion vp < setup vp
        test_function = Constrait().setup_constrait_battalion_VP
        test_camp = Iraq()
        test_battalion = [InfantryForce(), InfantryForce(), InfantryForce()]
        self.assertTrue(not test_function(test_camp, test_battalion))
        # case 2: total battalion = setup vp
        test_battalion2 = [InfantryForce(), InfantryForce(), InfantryForce(), InfantryForce(), MobileHQ(), 
            MobileHQ(), MobileHQ()]
        self.assertTrue(test_function(test_camp, test_battalion2))
        # case 3: total battalion > setup vp and it stops after that point
        test_battalion3 = [InfantryForce(), InfantryForce(), InfantryForce(), InfantryForce(), InfantryForce(), 
            InfantryForce()]
        self.assertTrue(test_function(test_camp, test_battalion3))
        # case 4: total battalion > setup vp and it doesnt stop
        test_battalion4 = [InfantryForce(), InfantryForce(), InfantryForce(), InfantryForce(), InfantryForce(), 
            InfantryForce(), InfantryForce()]
        self.assertTrue(not test_function(test_camp, test_battalion4))


if __name__ == '__main__':
    unittest.main()



