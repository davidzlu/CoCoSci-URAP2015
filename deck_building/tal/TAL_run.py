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
        #TODO: ADJUSTING/PROMOTING PILOTS NOT FULLY IMPLEMENTED
        pilots.promote_pilots(self.pilots, policy)
        print("Done selecting and promoting pilots")
        
        self.day_count = 1
        print("Setup complete, start-of-day setup begin")

    def setup_environment(self):
        sm = batt.SectorMap()
        self.total_vp = sm.get_all_enemies(self.campaign)
        #TODO: adjustment needed after inital placement, probably through special effects
        return sm
    
    def setup_enemy_units(self, game):
        return game.board.setup_enemy_units()
    
    def setup_friendly_units(self):
        pass
    
    def select_battalions_for_day(self):
        """Returns list of battalions to attack for the day based on self.policy
        TODO: WRITE THIS FUNCTION
        """
        return []
    
    def allocate_planes_and_pilots_to_missions(self, battalions_to_attack):
        """Assigns (plane, pilot) pairs to every battalion in battalions_to_attack.
        Returns dictionary mapping battalion->[list of (plane, pilot) pairs]
        TODO: DISCUSS PLAN FOR THIS WHOLE METHOD
        TODO: WRITE THIS FUNCTION
        """
        return {}
    
    def allocate_scouts(self):
        """Returns list of battalions that have been assigned a scout
        """ 
        return []
    
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
        self.day_missions = self.allocate_planes_and_pilots_to_misions(self.select_battalions_for_day())
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


def random_policy(gameInstance):
    """Pseudocode placeholder for what the policies should look like when written"""
    curphase = gameInstance.phase
    if curphase == "choose planes": #this comparator can be/should be changed
        choice = random.choice([True, False])
        if choice:
            choice = random.choice(planes.legal_actions(gameInstance.campaign))
        return choice
    elif curphase == "choose pilot":
        pilotList = []
        for plane in gameInstance.planes:
            choices = pilots.get_pilot_types(plane)
            chosenpilot = random.choice(choices)
            choices.remove(chosenpilot)
            pilotList.append(chosenpilot)
            # make a dictionary/set/list? of planes with pilots here or later?
        return pilots

