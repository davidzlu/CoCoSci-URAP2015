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
            if possible_placement:
                #just keep going, nothing wrong
                pass
            else:
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
            location = self.roll_to_location(roll) #TODO: do a roll -> location lookup, 
            #TODO: is there any other lookup involved? In Jasper and Zot, player can sometimes shift enemy tokens around
            # are all enemy units drawn in response to a roll? yes, or could later be addressed in constraints
            possible_placement = self.place_piece(unit, location, constraints)
            if possible_placement:
                #just keep going, nothing wrong
                pass
            else:
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
        #TODO: how to place pieces? should be in subclass. a location/tile/space interface?
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

    def game_loop(self, stage_order):
        #TODO: is this needed? essentially same as play?
        #stage_order -- list of methods, called in order that game should progress
        pass

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

    def play(self, policy):
        """Simulates a playthrough of the game using policy, returning a list
        of the form [[list of states visited],
                     [list of actions taken], 
                     [list of rewards received]].

        Parameters:
        policy -- a function defining a policy for the agent.
        """
        #TODO: figure out how much can be written here
        pass

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
    
    