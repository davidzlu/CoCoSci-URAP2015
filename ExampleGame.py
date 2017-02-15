'''Notes:
 - if constraints functions, should be able to call all right before needed rather than make list of functions
 - could also encapsulate constraints in a "phase constraints" function
 - maybe a method for each phase would make most conceptual sense
'''

from deck_building import DeckBuilding
import Features

class ExampleGame(DeckBuilding.DeckBuilding):
    '''
    An example game extending the DeckBuilding abstract class. For testing purposes and for serving as an example
    of what other games should look like.
    This game is a simplified version of Thunderbolt Apache Leader with the Iraq campaign wth Surge situation.
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        super(ExampleGame, self).__init__()
        self.situation = None
        self.campaign = None
        self.board = ExampleGameBoard()
        
    def setup_friendly_units(self, policy):
        pass
    
    def setup_enemy_units(self):
        pass
    
    def roll_to_location(self, roll):
        pass
    
    def setup_environment(self):
        pass
    
    def setup_random_events(self):
        pass
      
    def turn_setup_done(self):
        pass
    
    def play(self, policy):
        stage_order = []
        constraints = []
        self.play(policy, stage_order, constraints)
    
    def game_loop_done(self):
        pass
    
    def turn_setup(self, policy):
        pass
    
    def is_win_state(self):
        pass
    
    def is_lose_state(self):
        pass
    
    def transition_prob(self, action, next_state):
        pass
    
    def legal_actions(self):
        pass
    
    def reward(self, action):
        pass
    
    def next_states(self, action):
        pass
    
    ###############
    # Constraints #
    ###############
    
    
class ExampleGameBoard(DeckBuilding.Board):
    def __init__(self):
        pass
    
    def can_put_piece(self, piece, location, constraints):
        pass
    
    def place_piece(self, piece, location, constraints):
        pass
    
    
    
    
def main():
    features = Features.Features(ExampleGame)
    policy = None
    features.generateGames(policy, 100)
    features.generateFeatures("example_features.txt")

if __name__ == "__main__":
    main()
    