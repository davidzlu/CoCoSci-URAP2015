"""TODO: FIGURE OUT WHAT THIS INTERFAE IS LINKING.
What will be the subclasses. What information should they return.
Why do we need the outputs they give? What other class is accepting the 
results of the subclasses for this interface?
"""

import random


class DeckBuilding(object):
    """Abstract class for all deck building games.
    """

    tpm = {} # Maps (curState, action, nextState) to transition probability

    def __init__(self, setup_order):
        #TODO: what instance variables are needed for all games?
        #setup_order -- a list of methods, call each in order to setup board
        #could use same idea for play/game_loop function, or whatever does game loop
        self.board = None
        #assert type(self.board) == Board # if using Board interface, need this 
        self.friendly_units = []
        self.enemy_unit= []
        self.phase = 0
        
        self.states_visited = []
        self.actions_taken = []
        self.rewards_received = []
        
    #################
    # SETUP METHODS #
    #################
    
    def setup_friendly_units(self, policy):
        """Determines what friendly units can appear during gameplay.
        
        TODO: figure out parameters of this method
        
        e.g. in Jasper and Zot, getting Jasper piece. In TAL, selecting pilots, aircraft, and weapons.
        """
        raise NotImplementedError
    
    def place_friendly_units(self, units_to_place, constraints, policy):
        """Places all units in units_to_place on board during gameplay.
        Should be called after setup_friendly_units. Locations of pieces
        determined by policy.
        
        Parameters:
        units_to_place -- a list of units to place on the board
        constraints -- list of rules that must be satisfied when placing pieces
        policy -- a function that outputs locations for pieces
        """
        for unit in units_to_place:
            location = policy(unit) #TODO: figure out format of policies
            possible_placement = self.place_piece(unit, location, constraints)
            if not possible_placement:
                #anything needed?
                pass
            
    def setup_enemy_units(self):
        """Determines what enemy units can appear during gameplay.
        
        TODO: figure out parameters of this method
        
        e.g. In Jasper and Zot, equivalent to filling a bag with all the 
        enemy pieces.
        """
        raise NotImplementedError

    def place_enemy_units(self, units_to_place, constraints, dice_sides):
        """Places all units in units_to_place onto the board during gameplay.
        Should be called after setup_enemy_units. Places pieces based on
        a dice with dice_sides number of sides.

        e.g. In Jasper and Zot, equivalent to picking a piece from the bag
        and putting it on the board.

        Parameters:
        units_to_place -- list of pieces to place
        constraints -- list of constraints that must be satisfied when placing pieces
        dice_sides -- integer for number of sides on dice
        """
        for unit in units_to_place:
            roll = self.dice_roll(1, dice_sides)
            location = self.roll_to_location(roll)
            #TODO: is there any other lookup involved? In Jasper and Zot, player can sometimes shift enemy tokens around
            # are all enemy units drawn in response to a roll? yes, or could later be addressed in constraints
            possible_placement = self.place_piece(unit, location, constraints)
            if not possible_placement:
                #anything needed?
                pass
                
    def roll_to_location(self, roll):
        """Takes in a dice roll result and returns a location on the board.
        Must be overwritten in subclass.

        e.g. in JandZ, get the column zombies should be in after rolling
        Parameters:
        roll -- integer result of a dice roll
        """
        raise NotImplementedError

    def place_piece(self, piece, location, constraints):
        """Places piece onto location in board. Returns 1 if placed, 0 if
        was unable to.
        TODO: is it possible to be unable to place piece?
        e.g. zombies can be placed in this function, but pumpkins would not be

        Parameters:
        piece -- an enemy or friendly piece in the game
        location -- a location object?
        """
        #one idea: a board interface, locations pick out spaces on boards
        #w/o board interface/this delegation, entire method needs to be implemented in subclass
        placed = self.board.place_piece(piece, location, constraints)
        if placed:
            return 1
        else:
            #TODO: what should happen if you can't put piece in space?
            return 0

    def setup_environment(self):
        """Creates a board for the game, along with variables related to spaces
        on the board. Must be overwritten by subclasses.
        """
        raise NotImplementedError

#     def shuffle(self, pieces):
#         """Returns a shuffled version of pieces.
# 
#         Probably used for setup functions
#         Parameters:
#         pieces -- a list of pieces
#         """
#         shuffled_pieces = list(pieces)
#         random.shuffle(shuffled_pieces)
#         return shuffled_pieces

    def check_constraints(self, constraints):
        """Returns True if every contraint in constraints is satisfied.
        False otherwise.

        Parameters:
        constraints -- a list? of methods that return a boolean
        """
        for rule in constraints:
            if not rule(self):
                return False
        return True

    def pick_piece_from_pile(self, pieces):
        """Returns a random piece from pieces.
        
        Parameters:
        pieces -- a list of pieces to pick from. Should be friendly_units or enemy_units
        """
        if pieces == []:
            return None
        pieces.shuffle()
        return pieces.pop()
    
    def play(self, policy, stage_order, constraints):
        """Simulates a playthrough of the game using policy, returning a list (or maybe tuple)
        of the form [[list of states visited],
                     [list of actions taken], 
                     [list of rewards received]].

        Parameters:
        policy -- a function defining a policy for the agent.
        """
        #TODO: figure out how much can be written here
        self.states_visited = []
        self.actions_taken = []
        self.rewards_received = []
        #setup game
        #setup initial state of board
        while True:
            while not self.round_setup_done():
                self.round_setup()
                while self.game_loop_done():
                    self.game_loop(policy, stage_order, constraints)
            if self.is_lose_state():
                #TODO: Do lose state stuff
                break
            if self.is_win_state():
                #TODO: Do win state stuff
                break
        
        return [tuple(self.states_visited), tuple(self.actions_taken), tuple(self.rewards_received)]

    def game_loop(self, policy, stage_order, constraints):
        """Helper function for play. Implements stages of game loop. Goes through one iteration of the loop.
        TODO: is this needed? essentially same as play?
        
        Parameters:
        policy -- method that returns an action given current state
        stage_order -- list? of methods, called in order that game should progress
        constraints -- a dictionary? of boolean methods that must be called for a certain stage of the game loop
        """
        for stage_method in stage_order:
            """
            TODO: figure out what should happen for each round
            TODO: should tracking state be implemented in subclass? what should stage_method return?
            idea 1: all stage_methods return something. A state, action, and reward if it involves the agent.
                None if the stage doesn't involve the agent. Then check what was returned.
            idea 2: push state tracking down into stage_method implementation.
            """
            stage_method(self, policy, constraints[stage_method]) 
        pass
    
    def round_setup_done(self):
        """Returns true if setup for a round is finshed. Otherwise returns false.
        
        ex1: in TAL, checks if setup for a mission is finished
        ex2: in Jasper and Zot, checks if setting up next wave is done
        
        Parameters:
        TODO: figure out parameters
        """
        raise NotImplementedError
    
    def game_loop_done(self):
        """Returns true if the game loop should break. Otherwise returns false.
        
        ex1: in TAL, true if a mission is completely over and moving onto the next one, or if you lost or won
        ex2: in Jasper and Zot, true if a wave has finished, or if you lost or won.
        
        Parameters:
        TODO: figure out parameters
        """
        raise NotImplementedError
    
    def setup_round(self, policy):
        """Convenience method that calls relevant setup methods for starting a new "round" in the game.
        
        ex1: in TAL, called before starting a new mission
        ex2: in Jasper and Zot, called before starting a new wave
        
        Parameters:
        policy -- a function that returns an action for selecting and placing pieces
        TODO: figure out parameters
        """
        # self.setup_environment()
        # self.setup_friendly_units(policy)
        # self.setup_enemy_units()
        # self.place
        raise NotImplementedError

    def dice_roll(self, lo, hi):
        """Returns random integer in range [lo, hi].

        Parameters:
        lo -- lowest value in dice.
        hi -- highest value in dice.
        """
        return random.randint(lo, hi)

    def coin_flip(self):
        """Returns 0 or 1 with equal probability."""
        return self.dice_roll(0, 1)

    def transition_prob_matrix(self):
        """Returns this game's transition probability matrix."""
        return self.tpm

    def transition_prob_vector(self, action):
        """Returns row in transition probability matrix defined by (self, action).

        Parameters:
        action -- action taken in current state.
        """
        #TODO: write function
        pass

    def transition_prob(self, action, next_state):
        """Returns transition probability defined by (self, action, next_state).

        Parameters:
        action -- action taken in current state.
        next_state -- destination state after taking action in current state.
        """
        #TODO: figure out how much can be written here
        pass

    def is_win_state(self):
        """Returns True if self is a terminal state satisfying
        win conditions and False otherwise.
        Must be overwritten.
        """
        #TODO: figure out how much can be written here
        raise NotImplementedError

    def is_lose_state(self):
        """Returns True if self is a terminal state satisfying
        lose conditions and False otherwise.
        Must be overwritten.
        """
        #TODO: figure out how much can be written here
        raise NotImplementedError

    def legal_actions(self):
        """Returns list of all admissable actions the agent
        can take in current state.
        Must be overwritten.
        """
        #TODO: figure out how much can be written here
        raise NotImplementedError

    def reward(self, action):
        """Return reward received for taking action in current state.
        Must be overwritten.

        Parameters:
        action -- action taken in current state.
        """
        #TODO: figure out how much can be written here
        raise NotImplementedError

    def next_states(self, action):
        """Returns list of all possible states the agent
        can transition to after taking action in current state.
        Must be overwritten.

        Parameters:
        action -- action taken in current state.
        """
        #TODO: figure out how much can be written here
        raise NotImplementedError
    
    
class Board(object):
    """Interface for the boards of deck building games.
    May be simpler without this interface. Currently using it to track what methods would be nice to have
    when doing DeckBuilding setups. 
    """
    
    def can_put_piece(self, piece, location, constraints):
        """Returns true if piece is placed at location on the board and all constraints are satisfied.
        Returns false otherwise.
        
        Parameters:
        piece -- a piece to be placed on the board
        location -- a specified location on the board
        constraints -- rules that must be satisfied for the piece to be placed
        """
        raise NotImplementedError
    
    def place_piece(self, piece, location, constraints):
        """Places piece at location on board. Returns 1 if piece has been placed, 0 otherwise.
        
        Parameters:
        piece -- the piece to place
        location -- where on board to put piece
        constraints -- rules that must be satisfied for piece to be placed
        """
        raise NotImplementedError
    
    