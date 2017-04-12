from . import TAL_campaigns as camp
from . import TAL_situation as sit
from . import TAL_battalions as batt
from . import TAL_planes as planes
from . import TAL_pilots as pilots
from . import TAL_specialCondition as spec_cond
import deck_building.DeckBuilding.DeckBuilding as DeckBuilding
import random

class TALInstance(DeckBuilding):
    
    def __init__(self, campaign, situation, policy):
        assert type(campaign) in [camp.Iraq, camp.Libya11, camp.Libya84]
        assert type(situation) in [sit.Surge]
        super(TALInstance, self).__init__()
        self.campaign = campaign #A Campaign object, see TAL_campaigns
        self.situation = situation #A Situation object, see TAL_situation
        self.policy = policy
        self.special_condition_deck = spec_cond.generate_special_condition_deck() #A list of SpecialCondition objects, see TAL_specialCondition
          
        print("Drawing and placing battalions")
        self.total_vp = 0
        self.setup_environment() #A SectorMap object, see TAL_battalions.py
        print("Finished placing battalions")
        
        print("Selecting aircraft")
        self.planes = planes.get_all_planes(self, situation, policy) #A list of Plane objects, see TAL_planes
        self.scouts = self.situation.buy_scouts(policy) #A nonnegative integer
        print("Done selecting aircraft")
        
        print("Selecting and promoting pilots")
        self.pilots = pilots.select_pilots(self.planes, policy) #A list of Pilot objects, see TAL_pilots
        pilots.promote_pilots(self.pilots, policy)
        print("Done selecting and promoting pilots")
        
        self.day_count = 1
        print("Setup complete, start-of-day setup begin")

        self.day_missions = {}

    def setup_environment(self):
        self.sm = batt.SectorMap()
        self.total_vp = self.sm.total_vp
        #TODO: adjustment needed after inital placement, probably through special effects
    
    def setup_enemy_units(self, game):
        return game.board.setup_enemy_units()
    
    def setup_friendly_units(self):
        pass
    
    def allocate_planes_and_pilots_to_missions(self):
        """Chooses battalions to attack and assigns (plane, pilot) pairs to each chosen.
        Chooses a battalion and assigns planes one at a time.
        Updates self.day_missions, a dictionary mapping battalion->[list of (plane, pilot) pairs].
        TODO: WRITE THIS FUNCTION
        """
        policy = self.policy
        self.phase = "assign missions"
        self.day_missions = {}
        while policy(self) or len(self.day_missions) < 1: #Must have at least one mission
            #Choose battalion
            self.phase = "choose battalion"
            battalion = policy(self)

            #See if more missions wanted
            self.phase = "assign missions"
    
    def allocate_scouts(self):
        """Returns list of battalions that have been assigned a scout
        """
        policy = self.policy
        self.phase = "allocate scouts"
        scouted_missions = policy(self)
        return scouted_missions
    
    def day_setup(self):
        """Sets up variables at start of a day in TAL.
        This includes:
          - Drawing and resolving special condition
          - Selecting battalions to attack
          - Assigning pilots and aircraft to selected battalions
          - Allocating scouts
        """
        assert(len(self.special_condition_deck) > 0)
        self.day_special_condition = self.special_condition_deck.pop()
        #TODO: ACTIVATE SPECIAL CONDITION
        self.allocate_planes_and_pilots_to_misions()
        self.scouted_missions = self.allocate_scouts()
        
    def mission_setup(self):
        """Sets up a mission.
        This includes:
          - Abort mission option
          - Arm aircraft
          - Draw and resolve target-bound mission event
          - Engine damage check
          - Placing terrain hexes
          - Placing enemy units
          - Placing friendly aircraft
          - Checking scout success
          - Setting loiter turn count
        """
        #TODO: CHANGE PHASE OF GAME?
        #TODO: ABORT MISSION OPTION
        #TODO: APPLY RANGE BAND EFFECT
        #TODO: ARM AIRCRAFT
        #TODO: FUELING PRIORITY OPTION
        #TODO: TARGET-BOUND MISSION EVENT
        #TODO: ENGINE DAMAGE CHECK
        #TODO: PLACE TERRAIN HEXES
        #TODO: PLACE ENEMY UNITS, CHECKING IF BATTALION AT HALF STRENGTH
        #TODO: PLACE FRIENDY AIRCRAFT
        #TODO: SCOUT SUCCESS CHECK
        #TODO: SET LOITER COUNTER
        pass

    def loiter_turn_setup(self):
        """Sets up loiter turn.
        This includes:
          - Drawing pop-up counters
          - Enemy cover roll
        """
        pass
    
    def loiter_turn_setup_done(self):
        pass

"""Utility to check for bad input. Prompt should be a string while acceptable_answers should be a list of strings."""
def check_input(prompt, acceptable_answers):
    response = input(prompt)
    while response not in acceptable_answers:
        print("Your response did not match any of these: " + acceptable_answers)
        response = input("Please respond with one of the above options: ")
    return response

def human_policy_assign_missions(gameInstance):
    print(" - Will you continue choosing missions?")
    ans = ""
    answers = ("y", "n")
    while ans not in answers:
        ans = input(" - Your answer [y/n]: ")
        if ans not in answers:
            print("Please enter a valid choice.")
    if ans == "y":
        return True
    if ans == "n":
        return False
    
def select_planes_for_battalion(game_instance, battalion):
    print(" - Please pick a plane and pilot for this battalion.")
    
def human_policy_choose_battalion(game_instance):
    answers = ("y", "n")
    print(" - Starting mission selection.")
    print(" - Please pick a battalion.")
    active_batts = game_instance.sm.get_battalions_on_map()
    for active_batt in active_batts:
        if active_batt not in game_instance.day_missions:
            ans = ""
            while ans not in answers:
                ans = input(" - Select "+active_batt+active_batt.map_location+" [y/n]?")
                if ans == "y":
                    select_planes_for_battalion(game_instance, active_batt)
                elif ans not in answers:
                    print(" - Please enter a valid answer.")

def human_policy(gameInstance):
    curphase = gameInstance.phase
    if curphase == "choose planes":
        pass
    elif curphase == "choose pilots":
        pilotList = []
        planeTypes = set()
        for craft in gameInstance.planes:
            if craft.get_name() == 'RQ_1' or craft.get_name() == 'MQ_1':
                continue
            planeTypes.add(type(craft))
            choices = pilots.get_pilot_types(craft)
            print(choices)
            response = input("Select a pilot for your " + str(type(craft)))
            while response not in choices:
                response = input("Please enter a valid choice: ")
            pilot = pilots.get_pilot(response, "Average")
            while pilot in pilotList:
                print(choices)
                response = input("You've already chosen that pilot for another aircraft."
                                 "Please choose a different one: ")
                pilot = pilots.get_pilot(response, "Average")
            pilotList.append(pilot)
        for pType in planeTypes:
            choices = pilots.get_pilot_types(pType)
            print(choices)
            response = input("Please select an additional pilot for your " + str(type(pType)))
            while response not in choices:
                response = input("Please enter a valid choice: ")
            pilot = pilots.get_pilot(response, "Average")
            while pilot in pilotList:
                print(choices)
                response = input("You've already chosen that pilot for another aircraft."
                                 "Please choose a different one: ")
                pilot = pilots.get_pilot(response, "Average")
            pilotList.append(pilot)
        return pilotList
    elif curphase == "promote pilots":
        pilotList = gameInstance.pilots
        answers = ["y", "n"]
        phaseI = True
        phaseII = False
        while phaseI: #How many times you go through the pilots promoting and demoting
            newList = []
            for pilot in pilotList:
                print("Pilot: " + pilot.name)
                print("Skill Level: " + pilot.skill)
                response = input("Would you like to promote this pilot?: "
                                 "Answer with y or n: ")
                while response not in answers:
                    response = input("Please answer with y or n: ")
                if response == "y":
                    print("You must demote another pilot in exchange.")
                    flag = False #set to true once an equivalent demotion is made
                    for other_pilot in pilotList:
                        if other_pilot is pilot:
                            continue
                        elif flag:
                            newList.append(other_pilot)
                            continue
                        else:
                            print("Pilot: " + other_pilot.name)
                            print("Skill Level: " + other_pilot.skill)
                            demote = input("Demote this pilot?: ")
                            while demote not in answers:
                                demote = input("Please answer with y or n: ")
                            if demote == "y":
                                if (pilots.skill2num[other_pilot.skill] - 1) < 1:
                                    print("This pilot can not be demoted anymore.")
                                    newList.append(other_pilot)
                                    continue
                                elif (pilots.skill2num[pilot.skill] + 1) > 6:
                                    print("This pilot can not be promoted anymore.")
                                    newList.append(other_pilot)
                                    continue
                                else:
                                    promoted_skill = pilots.num2skill[pilots.skill2num[pilot.skill] + 1]
                                    promoted_p = pilots.get_pilot(pilot.name, promoted_skill)
                                    demoted_skill = pilots.num2skill[pilots.skill2num[other_pilot.skill] - 1]
                                    demoted_p = pilots.get_pilot(other_pilot.name, demoted_skill)
                                    newList.append(demoted_p)
                                    newList.append(promoted_p)
                                    flag = True
                            else:
                                newList.append(other_pilot)
                    if flag is False:
                        print("Pilot was not promoted.")
                        newList.append(pilot)
                else:
                    newList.append(pilot)
            pilotList = newList
            print("Would you like to continue promoting in exchange for demoting?")
            print("If you answer 'n', you will get a chance to promote in exchange for SO points.")
            cont = input("Answer with y or n: ")
            while cont not in answers:
                cont = input("Please answer with y or n: ")
            if cont == "n":
                phaseI = False

        p2 = input("Do you want to spend SO points to promote pilots?: ")
        while p2 not in answers:
            p2 = input("Please answer with y or n: ")
        if p2 == "y":
            phaseII = True
        while phaseII:
            newList = []
            for pilot in pilotList:
                print("Pilot: " + pilot.name)
                print("Skill Level: " + pilot.skill)
                print("Remaining SO points: " + gameInstance.situation.SOpoints)
                response = input("Would you like to promote this pilot?: "
                                 "Answer with y or n: ")
                while response not in answers:
                    response = input("Please answer with y or n: ")
                if response == "n":
                    newList.append(pilot)
                elif response == "y":
                    if (pilots.skill2num[pilot.skill] + 1) > 6:
                        print("This pilot can not be promoted anymore.")
                        newList.append(pilot)
                    elif gameInstance.situation.SOpoints < 1:
                        print("You don't have enough SO points.")
                        newList.append(pilot)
                    else:
                        gameInstance.situation.SOpoints -= 1
                        promoted_p = pilots.get_pilot(pilot.name, pilots.skill2num[pilot.skill] + 1)
                        newList.append(promoted_p)
            pilotList = newList
            print("Would you like to continue promoting in exchange for SO points?")
            cont = input("Answer with y or n: ")
            while cont not in answers:
                cont = input("Please answer with y or n: ")
            if cont == "n":
                phaseII = False
        gameInstance.pilots = pilotList
    elif curphase == "assign missions":
        return human_policy_assign_missions(gameInstance)
    elif curphase == "choose battalion":
        """For this block:
         - Check gameInstance.sm for active battalions
         - Choose battalions not in gameInstance.day_missions
         - return a battalion
        """
        return human_policy_choose_battalion(gameInstance)
    elif curphase == "allocate scouts":
        """For this block:
         - Loop through gameInstance.day_missions, decide to assign scout
         - Add scouted missions to a list
         - Return list of battalions with scouts
        """
        pass
    elif curphase == "abort mission":
        response = input("Do you wish to abort this mission? Answer with y or n: ")
        while response not in ["y", "n"]:
            response = input("Please answer either with y or n: ")
        if response == "y":
            return False
        return True
    elif curphase == "fueling priority":
        print("Would you like to purchase Fueling Priority for 1 SO point?")
        response = input("Please answer with y or n: ")
        while response not in ["y", "n"]:
            response = input("Please answer either with y or n: ")
        if response == "y":
            #go through and reduce weight penalty
            for mission in gameInstance.day_missions:
                pass # TODO: Adjust the weight penalty of each plane depending on the range band the battalion is in
            gameInstance.situation.SOpoints -= 1
    elif curphase == "arm aircraft":
        aircrafts = gameInstance.planes
        weapons = planes.weapon_pool.copy()
        totalOrdPts = 0
        SOpts_spent = 0
        for plane in aircrafts:
            SOpts_spent = totalOrdPts // 10
            if (totalOrdPts % 10) != 0:
                SOpts_spent += 1
            if SOpts_spent >= gameInstance.situation.SOpoints:
                print("You have spent all of your SO points.")
                break
            arm = True
            allowed = plane.weapon_set
            totalweight = plane.weight
            while totalweight > 0 and arm is True:
                print('Currently equipping' + plane.get_name())
                print('You have ' + totalweight + " weight points left.")
                print('These are your weapon choices: ')
                print(allowed)
                response = input("Select a weapon: ")
                while response not in allowed:
                    response = input("Please enter a valid choice: ")
                weapon = planes.get_weapon(response)
                print('This will cost you ' + weapon.weaponWeight + 'points and '
                      + weapon.ordnancePoints + ' ordnance points.')
                response2 = input('Is this okay? Answer with y or n: ')
                while response2 not in ['y', 'n']:
                    response2 = input("Please respond with either y or n: ")
                if response2 == 'n':
                    continue
                elif response2 == 'y':
                    if weapon.weaponWeight <= totalweight:
                        plane.weapons_equipped.append(weapon)
                        totalweight -= weapon.weaponWeight
                        totalOrdPts += weapon.ordnancePoints
                        weapons[response] -= 1 #Might need to also decrease the paired weapon
                    else:
                        print("This weapon is too heavy for the plane to carry.")
                done = input("Are you done equipping this plane? Answer with y or n: ")
                while done not in ['y', 'n']:
                    done = input("Please respond with either y or n: ")
                if done == 'y':
                    arm = False
        gameInstance.situation.SOpoints -= SOpts_spent
    elif curphase == "place aircraft":
        # should probably combine select altitude with this
        pass

def random_policy(gameInstance):
    """Pseudocode placeholder for what the policies should look like when written"""
    curphase = gameInstance.phase
    if curphase == "choose planes": #this comparator can be/should be changed
        choice = random.choice([True, False])
        if choice:
            choice = random.choice(planes.legal_actions(gameInstance.campaign))
        return choice
    elif curphase == "choose pilots":
        pilotList = []
        for plane in gameInstance.planes:
            choices = pilots.get_pilot_types(plane)
            chosenpilot = random.choice(choices)
            choices.remove(chosenpilot)
            pilotList.append(chosenpilot)
            # make a dictionary/set/list? of planes with pilots here or later?
        return pilots
    elif curphase == "promote pilots":
        pass
    elif curphase == "assign missions":
        pass
    elif curphase == "allocate scouts":
        pass
    elif curphase == "abort mission":
        pass
    elif curphase == "fueling priority":
        pass
    elif curphase == "arm aircraft":
        pass
    elif curphase == "place aircraft":
        #should probably combine select altitude with this
        pass


