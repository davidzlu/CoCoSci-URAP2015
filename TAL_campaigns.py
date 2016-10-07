# A Thunderbolt Apache Leader game file to interface with DeckBuilding.py
import random
from TAL_terrain import *

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




