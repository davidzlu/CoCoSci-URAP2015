"""TODO: File organizing so that we can dynamically drop further TAL files
into a folder and they will automatically all get imported into this run file

for reference: http://stackoverflow.com/questions/1057431/loading-all-modules-in-a-folder-in-python
"""
from TAL_campaigns import *

def setup_environment():
    sm = SectorMap()
    return sm

def setup_enemy_units(game):
    return game.board.setup_enemy_units()

def setup_friendly_units():
    pass
