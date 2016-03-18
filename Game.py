from abc import ABCMeta, abstractmethod
from peg_solitaire import *
from peg_markov import *

class Game(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def play(self, strategy):
        """Runs game with given strategy"""
        raise NotImplementedError("Must override")

    @abc.abstractmethod
    def possible_moves(self):
        """Returns the set of all possible moves given the current game state."""
        raise NotImplementedError("Must override")

    @abc.abstractmethod
    def next_states(self):
        """Returns the immediate states reachable from the current state"""
        raise NotImplementedError("Must override")

    @abc.abstractmethod
    def transition_prob_matrix(self):
        """Returns probability of transitioning from curState to nextState given action.
        """
        raise NotImplementedError("Must override")
        
    @abc.abstractmethod
    def isWinState(self):
        raise NotImplementedError("Must override")

    @abc.abstractmethod
    def isLoseState(self):
        raise NotImplementedError("Must override")
