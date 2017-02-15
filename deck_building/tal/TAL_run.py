from deck_building.tal import TAL_campaigns as camp
from deck_building.tal import TAL_situation as sit
from deck_building.tal import TAL_battalions as batt
from deck_building import DeckBuilding


class TALInstance(DeckBuilding.DeckBuilding):
    
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
        
        self.pilots = []
        self.planes = []
        
        #get_all_planes
        #get_plane_pilot
        #
    
    ##################
    # GETTER METHODS #
    ##################   
    
    def get_campaign_year(self):
        return self.campaign.year
    
    def get_campaign_vp(self):
        return self.campaign.setup_vp
    
    def get_campaign_terrain(self):
        return self.campaign.terrain_nums
    
    def get_campaign_eval(self):
        return self.campaign.eval
    
    def get_campaign_special(self):
        return None
        #return self.campaign.special
        
    def get_situation_so_points(self):
        return self.situation.SOpoints
    
    def get_situation_days(self):
        return self.situation.days
        
    def get_situation_daily_so(self):
        return self.situation.dailySO
    
    def get_situation_rules(self):
        return None
        #return self.situation.rules
    
    

    def setup_environment(self):
        sm = batt.SectorMap()
        self.total_vp = sm.get_all_enemies(self.campaign)
        #TODO: any adjustment needed after initla placement?
        return sm
    
    def setup_enemy_units(self, game):
        return game.board.setup_enemy_units()
    
    def setup_friendly_units(self):
        pass
    
    def turn_setup(self):
        pass
    
    def turn_setup_done(self):
        pass
