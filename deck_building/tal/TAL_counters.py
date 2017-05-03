from deck_building.tal.TAL_battalions import *

class PopUp:
    """22 No Enemy counters, 10 enemy counters"""
    def __init__(self, unit=None):
        if unit:
            unit.point_value = 0
        self.enemy_unit = unit



class Hit:

    def __init__(self, heavy, light, immunity, stress=0, attack=0):
        self.heavy = heavy
        self.light = light
        self.immunity = immunity # which planes are unaffected, use dict to distinguish between heavy and light sides
        self.stress = stress
        self.attack = attack


hit_counters = [Hit("bullet holes", "structure", {'heavy': None, 'light': 'AH_64'}),
                Hit("attack", "stress", {'heavy': None, 'light': 'A_10'}, 1, 2),
                Hit("structure", "structure", {'heavy': None, 'light': 'AV_8B'}),
                Hit("pylon", "stress", {'heavy': None, 'light': 'AH_64'}, 1),
                Hit("altitude", "stress", {'heavy': None, 'light': 'F_16'}, 2),
                Hit("killed", "engine", {'heavy': None, 'light': 'F_16'}),
                Hit("pylon", "cannon", {'heavy': 'F_16', 'light': 'A_10'})]