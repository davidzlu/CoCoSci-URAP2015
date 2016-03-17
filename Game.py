from abc import ABCMeta, abstractmethod
from peg_solitaire import *
from peg_markov import *

class Game(metaclass=ABCMeta):

	@abstractmethod
	def play(self, strategy):
		"""Runs game with given strategy"""

	@abstractmethod
	def possible_actions(self):
		"""Returns the set of all possible moves given the current game state."""

	@abstractmethod
	def next_states(self):
		"""Returns the immediate states reachable from the current state"""

	@abstractmethod
	def transition_prob_matrix(self):
		"""Returns probability of transitioning from curState to nextState given action.
        """
    # @abc.abstractmethod
    # def isWinState(self):

    # @abc.abstractmethod
    # def isLoseState(self):

#Game.register(PegSolitaire)

