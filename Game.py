import abc

class Game(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def play(self, strategy):
		"""Runs game with given strategy"""

	@abc.abstractmethod
	def possible_moves(self):
		"""Returns the set of all possible moves given the current game state."""

	@abc.abstractmethod
	def next_states(self):
		"""Returns the immediate states reachable from the current state"""

	@abc.abstractmethod
	def transition_prob_matrix(self):
		"""Returns probability of transitioning from curState to nextState given action.
        """
    @abc.abstractmethod
    def isWinState(self):

    @abc.abstractmethod
    def isLoseState(self):

    
