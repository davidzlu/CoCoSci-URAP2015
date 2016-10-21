# A Thunderbolt Apache Leader game file to interface with DeckBuilding.py


class Pilot:
    """Speed is 0 or 1 whether it is Slow or Fast.
        Status levels are 2=Okay, 1=Shaken, 0=Unfit

        stressScale is read as the upperbound of each status category.
        For example (17, 32) means that <= 17 means that the pilot is okay.
        18 <= shaken <=32, and >32 means unfit"""

    def __init__(self, name, skill, xp, actype, acname, speed,
                 strike, standoff, cool, stressScale, evasive=0, status=2, stress=0):
        self.name = name
        self.skill = skill
        self.xp = xp
        self.aircraftType = actype
        self.aircraftName = acname
        self.speed = speed
        self.strike = strike
        self.standoff = standoff
        self.cool = cool
        self.evasive = evasive
        self.status = status
        self.stress = stress
        self.stressScale = stressScale



def get_pilot(name, skill):
    if name == "Grandpa":
        if skill == "Newbie":
            return Pilot(name, skill, 6, "AH-1", "Cobra", 0, -1, 0, 0, (4, 5))
        elif skill == "Green":
            return Pilot(name, skill, 7, "AH-1", "Cobra", 0, 0, 1, 0, (5, 7))
        elif skill == "Average":
            return Pilot(name, skill, 8, "AH-1", "Cobra", 1, -1, 0, 0, (4, 6))
        elif skill == "Skilled":
            return Pilot(name, skill, 9, "AH-1", "Cobra", 1, 1, 0, 0, (5, 8))
        elif skill == "Veteran":
            return Pilot(name, skill, 10, "AH-1", "Cobra", 1, 1, 2, 0, (6, 9))
        elif skill == "Ace":
            return Pilot(name, skill, 100, "AH-1", "Cobra", 1, 1, 3, 1, (7, 11))
    elif name == "Viper":
        if skill == "Newbie":
            return Pilot(name, skill, 2, "A-10", "Thunderbolt", 0, -1, -1, 0, (3, 4))
        elif skill == "Green":
            return Pilot(name, skill, 3, "A-10", "Thunderbolt", 0, 0, 0, 0, (4, 6))
        elif skill == "Average":
            return Pilot(name, skill, 7, "A-10", "Thunderbolt", 1, 0, -1, 0, (4, 5))
        elif skill == "Skilled":
            return Pilot(name, skill, 8, "A-10", "Thunderbolt", 1, 1, 0, 0, (5, 7))
        elif skill == "Veteran":
            return Pilot(name, skill, 10, "A-10", "Thunderbolt", 1, 1, 1, 0, (5, 7), 1)
        elif skill == "Ace":
            return Pilot(name, skill, 100, "A-10", "Thunderbolt", 1, 2, 2, 0, (6, 10), 1)
    elif name == "Rock":
        if skill == "Newbie":
            return Pilot(name, skill, 2, "AH-64", "Apache", 0, -1, -1, 0, (3, 4))
        elif skill == "Green":
            return Pilot(name, skill, 4, "AH-64", "Apache", 0, 0, 0, 0, (5, 7))
        elif skill == "Average":
            return Pilot(name, skill, 5, "AH-64", "Apache", 0, 0, 1, 0, (7, 12))
        elif skill == "Skilled":
            return Pilot(name, skill, 8, "AH-64", "Apache", 0, 1, 1, 1, (9, 15))
        elif skill == "Veteran":
            return Pilot(name, skill, 11, "AH-64", "Apache", 0, 2, 2, 1, (9, 16))
        elif skill == "Ace":
            return Pilot(name, skill, 100, "AH-64", "Apache", 0, 2, 2, 2, (12, 22))

def get_pilot_types(aircrafttype):
    if aircrafttype == "AH-1":
        return ["Gator", "Grandpa", "Scuttle"]
    elif aircrafttype == "A-10":
        return ["Pirate", "Viper"]
    elif aircrafttype == "AH-64":
        return ["Hammer", "Judge", "Rock"]


def select_pilots(aircraftList):
    pilotList = []
    for craft in aircraftList:
        #get aircraft type to pass into get_pilot_types
        #pass pilot name and "Average" into get_pilot and append to pilotList
        pass
    return pilotList