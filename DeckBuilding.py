"""TODO: FIGURE OUT WHAT THIS INTERFAE IS LINKING.
What will be the subclasses. What information should they return.
Why do we need the outputs they give? What other class is accepting the 
results of the subclasses for this interface?
"""



class DeckBuilding(object):

    tpm = {} # Maps (curState, action, nextState) to transition probability

    def __init__(self, setup_order):
        #TODO: what instance variables are needed for all games?
        #setup_order -- a list of methods, call each in order to setup board
        #could use same idea for play/game_loop function, or whatever does game loop
        self.board = []
        self.friendly_units = []
        self.enemy_units = []
        self.phase = 0
        
    def create_board(self):
        """Creates a board for the game. Most general version here.
        May be overwritten by subclasses.

        Idea 1: subclass passes in board layout, this method turns it into data structure (e.g. a list)
          -lots of work passed down, not much reused
        Idea 2: pass in rows, columns, and a "period" so every other row has x columns/rows while others have y columns/rows
          -assumes all boards can be described periodically

        
        """

        pass

    def setup_friendly_units(self):
        """
        """
        raise NotImplementedError

    def pick_piece_from_pile(self):
        raise NotImplementedError

    def setup_enemy_units(self):
        """
        """
        raise NotImplementedError

    def setup_environment(self):
        """
        """
        raise NotImplementedError

    def shuffle(self, pieces):
        """Returns a shuffled version of pieces.

        Probably used for setup functions
        Parameters:
        pieces -- a list of pieces
        """
        #TODO: write function
        pass

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
        #TODO: write function
        pass

    def coin_flip(self):
        """Returns 0 or 1 with equal probability."""
        #TODO: write function
        pass

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