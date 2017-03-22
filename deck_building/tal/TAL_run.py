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
        self.sm = self.setup_environment() #A SectorMap object, see TAL_battalions.py
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
        sm = batt.SectorMap()
        self.total_vp = sm.get_all_enemies(self.campaign)
        #TODO: adjustment needed after inital placement, probably through special effects
        return sm
    
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
        while policy(self) and len(self.day_missions) < 1: #Must have at least one mission
            #Choose battalion
            self.phase = "choose battalion"
            battalion = policy(self)
            
            #Choose planes
            self.phase = "assign planes"
            planes = policy(self)
            
            assert(battalion not in self.day_missions)
            self.day_missions[battalion] = planes
                        
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
    elif curphase == "promote pilots": #returns True or False depending on success
        pilotList = gameInstance.pilots
        # if these two numbers aren't equal, the difference will be the number of so points spent.
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
                # Below only works with one level of promotion/demotion
                if response == "promote":
                    promotions += 1
                    pilot = pilots.get_pilot(pilot.name, "Skilled")
                    response2 = input("Would you like to promote again? Please answer with y or n: ")
                    while response2 not in answers:
                        response2 = input("Please answer with y or n: ")
                    if response2 == "y":
                        promotions += 1
                        pilot = pilots.get_pilot(pilot.name, "Veteran")
                        response2 = input("Would you like to promote again? Please answer with y or n: ")
                        while response2 not in answers:
                            response2 = input("Please answer with y or n: ")
                        if response2 == "y":
                            promotions += 1
                            pilot = pilots.get_pilot(pilot.name, "Ace")
                elif response == "demote":
                    demotions += 1
                    pilot = pilots.get_pilot(pilot.name, "Green")
                    response2 = input("Would you like to promote again? Please answer with y or n: ")
                    while response2 not in answers:
                        response2 = input("Please answer with y or n: ")
                    if response2 == "y":
                        demotions += 1
                        pilot = pilots.get_pilot(pilot.name, "Newbie")
            pilotList.append(pilot)
        #calculate how many points spent on promotion/demotion
        SOpts_spent = abs(promotions - demotions)
        if SOpts_spent > gameInstance.situation.SOpoints:
            print("You've spent too many SO points during promotion. Please try again.")
            return False
        gameInstance.situation.SOpoints -= SOpts_spent
        gameInstance.pilots = pilotList
        return True
    elif curphase == "assign missions":
        """For this block:
         - Decide whether to continue choosing missions
         - Return True/False
        """
        pass
    elif curphase == "choose battalion":
        """For this block:
         - Check gameInstance.sm for active battalions
         - Choose battalions not in gameInstance.day_missions
         - return a battalion
        """
        pass
    elif curphase == "assign planes":
        """For this block:
         - adjust weight penalty
        """
        pass
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


