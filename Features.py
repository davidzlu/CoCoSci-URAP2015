class Features:

	def __init__(self, game):
		self.game = game

	def entropy(self, prob_matrix):
		"""
		Parameters:
		  prob_matrix: the transition probability matrix for the game
		Returns entropy of outcome distribution.
		https://en.wikipedia.org/wiki/Entropy_%28information_theory%29#Definition
		"""
		return 0

	def possibleActions(self, actF):
		"""
		Parameters:
		  actF: a function that returns possible actions.
		Returns number of possible actions in game.
		"""
		return 0

	def winToFinal(self):
		"""
		Returns ratio of win states to final states.
		"""
		return 0

	def loseToFinal(self):
		"""
		Returns ratio of lose states to final states.
		"""
		return 0

	def movesToFinal(self):
		"""
		Returns average number of moves before reaching a final state.
		"""
		return 0