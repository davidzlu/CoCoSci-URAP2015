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
        pieces.append(get_tile(piece)) #get piece will be found in the terrain file
    board = [list(pieces[0:3]), list(pieces[3:7]), list(pieces[7:])]
    set_adjacent_tiles(board)
    return board

def set_adjacent_tiles(tilelist):
    p1 = tilelist[0][0]
    p2 = tilelist[0][1]
    p3 = tilelist[0][2]
    p4 = tilelist[1][0]
    p5 = tilelist[1][1]
    p6 = tilelist[1][2]
    p7 = tilelist[1][3]
    p8 = tilelist[2][0]
    p9 = tilelist[2][1]
    p10 = tilelist[2][2]

    p1.bnext = p2
    p1.cnext = p5
    p1.dnext = p4
    
    p2.bnext = p3
    p2.cnext = p6
    p2.dnext = p5
    p2.enext = p1
    
    p3.cnext = p7
    p3.dnext = p6
    p3.enext = p2
    
    p4.anext = p1
    p4.bnext = p5
    p4.cnext = p8
    
    p5.anext = p2
    p5.bnext = p6
    p5.cnext = p9
    p5.dnext = p8
    p5.enext = p4
    p5.fnext = p1

    p6.anext = p3
    p6.bnext = p7
    p6.cnext = p10
    p6.dnext = p9
    p6.enext = p5
    p6.fnext = p2

    p7.dnext = p10
    p7.enext = p6
    p7.fnext = p3
    
    p8.anext = p5
    p8.bnext = p9
    p8.fnext = p4

    p9.anext = p6
    p9.bnext = p10
    p9.enext = p8
    p9.fnext = p5

    p10.anext = p7
    p10.enext = p9
    p10.fnext = p6

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

    def setup_constrait_batallion_cycle(self, battalion):
        """check if the battalion cards that are selected is in sequence of:
            assault, assault, support, command."""
        check_list = ["A", "A", "S", "C"]
        for i in range(0, len(battalion)):
            if battalion[i].type[1] != check_list[i % 4]:
                return False
        return True

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

    def test_setup_constrait_battalion_cycle(self):
        test_function = Constrait().setup_constrait_batallion_cycle
        # case 1: succeed
        test_battalion = [InfantryForce(), InfantryForce(), EngineerUnit(), HeadQuarters()]
        self.assertTrue(test_function(test_battalion))
        # case 2: failed
        test_battalion2 = [InfantryForce(), InfantryForce(), HeadQuarters(), EngineerUnit()]
        self.assertTrue(not test_function(test_battalion2))


if __name__ == '__main__':
    unittest.main()



