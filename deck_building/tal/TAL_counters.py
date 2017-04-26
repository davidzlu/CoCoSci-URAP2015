from deck_building.tal.TAL_battalions import *

class PopUp:
    """22 No Enemy counters, 10 enemy counters"""
    def __init__(self, unit=None):
        if unit:
            unit.point_value = 0
        self.enemy_unit = unit


