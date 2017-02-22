from . import TAL_campaigns as camp
from . import TAL_situation as sit
from . import TAL_battalions as batt
from . import TAL_planes as planes
from . import TAL_pilots as pilots
import deck_building.DeckBuilding.DeckBuilding as DeckBuilding

class TALInstance(DeckBuilding):
    
    def __init__(self, campaign, situation, policy):
        assert type(campaign) in [camp.Iraq, camp.Libya11, camp.Libya84]
        assert type(situation) in [sit.Surge]
        super(TALInstance, self).__init__()
        self.campaign = campaign
        self.situation = situation
        print("Drawing and placing battalions")
        self.total_vp = 0
        self.sm = self.setup_environment()
        print("Finished placing battalions")
        
        print("Selecting aircraft")
        self.planes = []
        #TODO: FIGURE OUT HOW POLICIES IMPLEMENTED
        pick_policy = None
        halting_policy = None
        self.planes = planes.get_all_planes(campaign, situation, pick_policy, halting_policy)
        self.scouts = self.situation.buy_scouts(policy())
        print("Done selecting aircraft")
        
        print("Selecting and promoting pilots")
        self.pilots = []
        self.pilots = pilots.select_pilots(self.planes, policy)
        #TODO: ADJUSTING (NOT PROMOTING) PILOTS NOT IMPLMENTED
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
    
    def turn_setup(self):
        pass
    
    def turn_setup_done(self):
        pass
