# A Thunderbolt Apache Leader game file to interface with DeckBuilding.py
from TAL_planes import *

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
    elif name == "Freak":
        if skill == "Newbie":
            return Pilot(name, skill, 2, "AH-1", "Cobra", 0, -1, -1, 0, (3, 4))
        elif skill == "Green":
            return Pilot(name, skill, 3, "AH-1", "Cobra", 0, 0, 0, 0, (4, 6))
        elif skill == "Average":
            return Pilot(name, skill, 6, "AH-1", "Cobra", 0, 0, 1, 0, (4, 6), 1)
        elif skill == "Skilled":
            return Pilot(name, skill, 8, "AH-1", "Cobra", 0, 1, 1, 1, (5, 8), 1)
        elif skill == "Veteran":
            return Pilot(name, skill, 9, "AH-1", "Cobra", 0, 2, 1, 1, (7, 12), 1)
        elif skill == "Ace":
            return Pilot(name, skill, 100, "AH-1", "Cobra", 0, 2, 2, 2, (9, 15), 1)
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
    elif name == "Zinger":
        if skill == "Newbie":
            return Pilot(name, skill, 6, "AC-130", "Spectre", 0, None, -1, 0, (2, 3), 5)
        elif skill == "Green":
            return Pilot(name, skill, 6, "AC-130", "Spectre", 0, None, 0, 0, (5, 7), 6)
        elif skill == "Average":
            return Pilot(name, skill, 8, "AC-130", "Spectre", 0, None, 1, 0, (5, 8), 7)
        elif skill == "Skilled":
            return Pilot(name, skill, 8, "AC-130", "Spectre", 0, None, 1, 0, (7, 12), 8)
        elif skill == "Veteran":
            return Pilot(name, skill, 12, "AC-130", "Spectre", 1, None, 2, 0, (7, 12), 9)
        elif skill == "Ace":
            return Pilot(name, skill, 100, "AC-130", "Spectre", 1, None, 2, 1, (8, 14), 10)
    elif name == "Neon":
        if skill == "Newbie":
            return Pilot(name, skill, 4, "AC-130", "Spectre", 0, None, -1, 0, (2, 3), 3)
        elif skill == "Green":
            return Pilot(name, skill, 4, "AC-130", "Spectre", 0, None, 0, 0, (5, 7), 4)
        elif skill == "Average":
            return Pilot(name, skill, 6, "AC-130", "Spectre", 0, None, 1, 1, (6, 9), 5)
        elif skill == "Skilled":
            return Pilot(name, skill, 7, "AC-130", "Spectre", 1, None, 1, 1, (5, 8), 6)
        elif skill == "Veteran":
            return Pilot(name, skill, 9, "AC-130", "Spectre", 1, None, 1, 1, (7, 12), 7)
        elif skill == "Ace":
            return Pilot(name, skill, 100, "AC-130", "Spectre", 1, None, 2, 2, (9, 15), 8)
    elif name == "Mohawk":
        if skill == "Newbie":
            return Pilot(name, skill, 4, "F-16", "Fighting Falcon", 0, 0, -1, 0, (2, 3))
        elif skill == "Green":
            return Pilot(name, skill, 3, "F-16", "Fighting Falcon", 0, 0, 0, 0, (4, 6))
        elif skill == "Average":
            return Pilot(name, skill, 8, "F-16", "Fighting Falcon", 1, -1, 0, 0, (4, 6))
        elif skill == "Skilled":
            return Pilot(name, skill, 8, "F-16", "Fighting Falcon", 1, 0, 0, 0, (6, 10))
        elif skill == "Veteran":
            return Pilot(name, skill, 9, "F-16", "Fighting Falcon", 1, 1, 1, 0, (8, 13))
        elif skill == "Ace":
            return Pilot(name, skill, 100, "F-16", "Fighting Falcon", 1, 2, 2, 1, (8, 13))
    elif name == "Dart":
        if skill == "Newbie":
            return Pilot(name, skill, 5, "F-16", "Fighting Falcon", 0, -1, 0, 0, (3, 4))
        elif skill == "Green":
            return Pilot(name, skill, 6, "F-16", "Fighting Falcon", 0, 0, 1, 0, (4, 6))
        elif skill == "Average":
            return Pilot(name, skill, 6, "F-16", "Fighting Falcon", 0, 1, 1, 0, (6, 10))
        elif skill == "Skilled":
            return Pilot(name, skill, 9, "F-16", "Fighting Falcon", 0, 2, 2, 0, (6, 10))
        elif skill == "Veteran":
            return Pilot(name, skill, 9, "F-16", "Fighting Falcon", 0, 2, 2, 1, (8, 14))
        elif skill == "Ace":
            return Pilot(name, skill, 100, "F-16", "Fighting Falcon", 0, 3, 3, 1, (8, 13))
    elif name == "Halo":
        if skill == "Newbie":
            return Pilot(name, skill, 4, "A-10", "Thunderbolt", 0, -1, 0, 0, (3, 4))
        elif skill == "Green":
            return Pilot(name, skill, 4, "A-10", "Thunderbolt", 0, -1, 0, 1, (5, 7))
        elif skill == "Average":
            return Pilot(name, skill, 6, "A-10", "Thunderbolt", 0, 0, 0, 1, (8, 13))
        elif skill == "Skilled":
            return Pilot(name, skill, 4, "A-10", "Thunderbolt", 0, 0, 0, 1, (9, 15), 1)
        elif skill == "Veteran":
            return Pilot(name, skill, 4, "A-10", "Thunderbolt", 0, 1, 0, 2, (9, 16), 1)
        elif skill == "Ace":
            return Pilot(name, skill, 100, "A-10", "Thunderbolt", 0, 2, 1, 2, (12, 21), 1)
    elif name == "Thor":
        if skill == "Newbie":
            return Pilot(name, skill, 3, "A-10", "Thunderbolt", 0, -1, -1, 0, (5, 6))
        elif skill == "Green":
            return Pilot(name, skill, 5, "A-10", "Thunderbolt", 0, 1, 0, 0, (5, 6))
        elif skill == "Average":
            return Pilot(name, skill, 6, "A-10", "Thunderbolt", 0, 2, 0, 0, (6, 9))
        elif skill == "Skilled":
            return Pilot(name, skill, 8, "A-10", "Thunderbolt", 0, 2, 0, 0, (7, 11), 1)
        elif skill == "Veteran":
            return Pilot(name, skill, 10, "A-10", "Thunderbolt", 0, 3, 1, 0, (7, 11), 1)
        elif skill == "Ace":
            return Pilot(name, skill, 100, "A-10", "Thunderbolt", 0, 3, 2, 1, (9, 15), 1)
    elif name == "Gumby":
        if skill == "Newbie":
            return Pilot(name, skill, 4, "A-10", "Thunderbolt", 0, -1, 0, 0, (3, 4))
        elif skill == "Green":
            return Pilot(name, skill, 4, "A-10", "Thunderbolt", 0, -1, 1, 0, (6, 8))
        elif skill == "Average":
            return Pilot(name, skill, 6, "A-10", "Thunderbolt", 0, 0, 2, 0, (6, 9))
        elif skill == "Skilled":
            return Pilot(name, skill, 6, "A-10", "Thunderbolt", 0, 0, 2, 1, (8, 12))
        elif skill == "Veteran":
            return Pilot(name, skill, 9, "A-10", "Thunderbolt", 0, 3, 1, 0, (8, 13))
        elif skill == "Ace":
            return Pilot(name, skill, 100, "A-10", "Thunderbolt", 0, 3, 2, 1, (9, 15))
    elif name == "Rebel":
        if skill == "Newbie":
            return Pilot(name, skill, 2, "A-10", "Thunderbolt", 0, -1, -1, 0, (4, 5))
        elif skill == "Green":
            return Pilot(name, skill, 3, "A-10", "Thunderbolt", 0, 0, 0, 0, (5, 7))
        elif skill == "Average":
            return Pilot(name, skill, 6, "A-10", "Thunderbolt", 0, 0, 1, 0, (5, 7), 1)
        elif skill == "Skilled":
            return Pilot(name, skill, 8, "A-10", "Thunderbolt", 0, 1, 1, 1, (6, 9), 1)
        elif skill == "Veteran":
            return Pilot(name, skill, 9, "A-10", "Thunderbolt", 0, 1, 2, 1, (8, 13), 1)
        elif skill == "Ace":
            return Pilot(name, skill, 100, "A-10", "Thunderbolt", 0, 2, 2, 1, (7, 11), 2)
    elif name == "Hack":
        if skill == "Newbie":
            return Pilot(name, skill, 4, "AV-8B", "Harrier", 0, 0, -1, 0, (3, 4))
        elif skill == "Green":
            return Pilot(name, skill, 4, "AV-8B", "Harrier", 0, 0, 0, 0, (6, 8))
        elif skill == "Average":
            return Pilot(name, skill, 7, "AV-8B", "Harrier", 0, 0, 1, 0, (6, 8), 1)
        elif skill == "Skilled":
            return Pilot(name, skill, 9, "AV-8B", "Harrier", 0, 1, 1, 1, (7, 10), 1)
        elif skill == "Veteran":
            return Pilot(name, skill, 10, "AV-8B", "Harrier", 0, 1, 2, 1, (9, 14), 1)
        elif skill == "Ace":
            return Pilot(name, skill, 100, "AV-8B", "Harrier", 0, 1, 2, 1, (10, 16), 2)
    elif name == "Pro":
        if skill == "Newbie":
            return Pilot(name, skill, 4, "AV-8B", "Harrier", 0, -1, 0, 0, (3, 4))
        elif skill == "Green":
            return Pilot(name, skill, 4, "AV-8B", "Harrier", 0, -1, 1, 0, (6, 8))
        elif skill == "Average":
            return Pilot(name, skill, 8, "AV-8B", "Harrier", 1, -1, 0, 0, (5, 7))
        elif skill == "Skilled":
            return Pilot(name, skill, 10, "AV-8B", "Harrier", 1, 0, 1, 0, (7, 10))
        elif skill == "Veteran":
            return Pilot(name, skill, 10, "AV-8B", "Harrier", 1, 0, 2, 0, (8, 13))
        elif skill == "Ace":
            return Pilot(name, skill, 100, "AV-8B", "Harrier", 1, 1, 3, 0, (10, 16))
    elif name == "Genius":
        if skill == "Newbie":
            return Pilot(name, skill, 5, "AV-8B", "Harrier", 0, 0, -1, 0, (4, 5))
        elif skill == "Green":
            return Pilot(name, skill, 6, "AV-8B", "Harrier", 0, 0, 0, 1, (5, 7))
        elif skill == "Average":
            return Pilot(name, skill, 6, "AV-8B", "Harrier", 0, 1, 0, 1, (7, 10))
        elif skill == "Skilled":
            return Pilot(name, skill, 8, "AV-8B", "Harrier", 0, 2, 0, 1, (9, 14))
        elif skill == "Veteran":
            return Pilot(name, skill, 9, "AV-8B", "Harrier", 0, 3, 0, 1, (10, 15))
        elif skill == "Ace":
            return Pilot(name, skill, 100, "AV-8B", "Harrier", 0, 3, 1, 2, (12, 21))
    elif name == "Divot":
        if skill == "Newbie":
            return Pilot(name, skill, 3, "AV-8B", "Harrier", 0, -1, 0, 0, (2, 3))
        elif skill == "Green":
            return Pilot(name, skill, 4, "AV-8B", "Harrier", 0, 0, 1, 0, (4, 5))
        elif skill == "Average":
            return Pilot(name, skill, 6, "AV-8B", "Harrier", 0, 0, 2, 0, (6, 9))
        elif skill == "Skilled":
            return Pilot(name, skill, 7, "AV-8B", "Harrier", 0, 0, 3, 0, (7, 10))
        elif skill == "Veteran":
            return Pilot(name, skill, 8, "AV-8B", "Harrier", 0, 1, 3, 1, (8, 12))
        elif skill == "Ace":
            return Pilot(name, skill, 100, "AV-8B", "Harrier", 0, 2, 3, 2, (10, 16))


def get_pilot_types(aircrafttype):
    if type(aircrafttype) is AH_1:
        return ["Gator", "Grandpa", "Scuttle", "Freak"]
    elif (type(aircrafttype) is A_10A) or (type(aircrafttype) is A_10C):
        return ["Pirate", "Viper", "Gumby", "Halo", "Thor", "Rebel"]
    elif (type(aircrafttype) is AH_64A) or (type(aircrafttype) is AH_64D):
        return ["Hammer", "Judge", "Rock", "Montana", "Shadow", "Daddy-O", "Eagle",
                "Tex", "Flash", "Cougar"]
    elif type(aircrafttype) is F_16:
        return ["Dart", "Mohawk"]
    elif type(aircrafttype) is AC_130:
        return ["Neon", "Zinger"]
    elif type(aircrafttype) is AV_8B:
        return ["Divot", "Genius", "Hack", "Pro"]


def select_pilots(aircraftList, strategy):
    pilotList = []
    for craft in aircraftList:
        choices = get_pilot_types(craft)
        # strategy(choices)
        # following code is for human player
        print(choices)
        response = input("Select a pilot for your " + type(craft))
        while response not in choices:
            response = input("Please enter a valid choice: ")
        pilot = get_pilot(response, "Average")
        while pilot in pilotList:
            print(choices)
            response = input("You've already chosen that pilot for another aircraft."
                             "Please choose a different one.: ")
            pilot = get_pilot(response, "Average")
        pilotList.append(pilot)
    return pilotList

def promote_pilots(pilotList):
    #This code currently only works for the setup portion
    pilotList = []
    #if these two numbers aren't equal, the difference will be the number of so points spent.
    promotions = 0
    demotions = 0
    answers = ["y", "n", "promote", "demote"]
    for pilot in pilotList:
        response = input("Would you like to promote or demote this pilot? "
                         "Answer with y or n: ")
        while response not in answers:
            response = input("Please answer with y or n: ")
        if response == "y":
            response = input("Please answer with either 'promote' or 'demote'."
                             "If you've changed your mind, you may answer with 'n': ")
            while response not in answers:
                response = input("Please answer with 'promote' or 'demote' or 'n': ")
            if response == "promote":
                promotions += 1
                pilot = get_pilot(pilot.name, "Skilled")
            elif response == "demote":
                demotions += 1
                pilot = get_pilot(pilot.name, "Green")
        pilotList.append(pilot)
    return pilotList, promotions, demotions