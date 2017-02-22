from . import TAL_campaigns as camp
from . import TAL_situation as sit
from . import TAL_battalions as batt
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
        self.scouts = 0
        print("Done selecting aircraft")
        
        print("Selecting pilots")
        self.pilots = []
        print("Done selecting pilots")
        #get_all_planes
        #get_plane_pilot
        #

    def setup_environment(self):
        sm = batt.SectorMap()
        self.total_vp = sm.get_all_enemies(self.campaign)
        #TODO: adjustment needed after initla placement
        return sm
    
    def setup_enemy_units(self, game):
        return game.board.setup_enemy_units()
    
    def setup_friendly_units(self):
        pass
    
    def turn_setup(self):
        pass
    
    def turn_setup_done(self):
        pass
