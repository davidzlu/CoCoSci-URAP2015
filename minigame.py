import random
import numpy as np
import ast
from itertools import permutations

def create_mini_game(row, column):
	"""create empty board for minigames"""
	board = np.zeros([row, column])
	return board

def roll_dice(n):
	"""roll n dices at once"""
	result = []
	for i in range(0, n):
		roll = random.randint(1, 6)
		result.append(roll)
	return result

def randomPolicy(state):
	""" Generates next legal action for agent to take.
		Arguments:
			state: The current state for which an action will be generated.
	"""
	legalMoves = state.legalActions()
	return random.choice(legalMoves)

class Minigame:
	"""a class for the minigames for Utopia Engine"""
	def __init__(self, row, column):
		"""initial state for minigame"""
		self.board = create_mini_game(row, column)

	def roll_dice_get_number(n):
		"""get number for each step"""
		return roll_dice(n)

	def check_full(self):
		"""check if the minigame board is full"""
		return np.count_nonzero(self.board) == self.board.size

	def play(self):
		return

	def check_final_range(self):
		if self.check_full():
			return 0

class Search(Minigame):
	"""Class for search minigame.
	"""

	def play(self, policy):
		"""Play through one search round. Returns final difference after filling in board.
			Arguments:
				policy: a function that takes in the current state and returns a legal action
		"""
		while not self.check_full():
			rolls = roll_dice_get_number(2)
			nextMove = policy(self)


	def legalActions(self):
		"""Returns list of ways a pair of numbers can be placed on the board.
			Moves represented as list of form:
				[(row, column) 1st number goes, (row, column) 2nd number goes]
		"""
		emptySpaces = []
		for row in self.board:
			for space in row:
				if space == -1:
					emptySpaces.append((row, space))

		# List of all pairs of spaces with repeats
		# e.g. permutations([1, 2, 3], 2) returns [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
		actions = list(permutations(emptySpaces, 2))
		return actions


