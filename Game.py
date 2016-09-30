from abc import ABCMeta, abstractmethod

class Game(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def play(self, strategy):
        """Runs game with given strategy"""
        raise NotImplementedError("Must override")

    @abstractmethod
    def possible_actions(self):
        """Returns the set of all possible actions given the current game state."""
        raise NotImplementedError("Must override")

    @abstractmethod
    def next_states(self):
        """Returns the immediate states reachable from the current state"""
        raise NotImplementedError("Must override")

    @abstractmethod
    def transition_prob_matrix(self):
        """Returns probability of transitioning from curState to nextState given action.
        """
        raise NotImplementedError("Must override")

    def transition_prob_vector(self, action):
        raise NotImplementedError("Must override")

    def transition_prob(self, action, next_state):
        raise NotImplementedError("Must override")

    def reward(self, action):
        raise NotImplementedError("Must override")
        
    @abstractmethod
    def isWinState(self):
        raise NotImplementedError("Must override")

    @abstractmethod
    def isLoseState(self):
        raise NotImplementedError("Must override")
