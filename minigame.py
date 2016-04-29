import random
import numpy as np
import ast
from itertools import permutations, combinations_with_replacement, combinations

def create_mini_game(row, column):
	"""create empty board for minigames"""
	board = np.zeros((row, column))
	return board.astype(int)


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

	def roll_dice_get_number(self, n):
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

	def put_number(self, num, row, column):
		assert row < self.board.shape[0] and column < self.board.shape[1]
		self.board[row][column] = num

class Activation(Minigame):
	def __init__(self):
		"""create a 2*4 board"""
		Minigame.__init__(self, 2, 4)
	
	def roll_dice_get_number(self):
		Minigame.roll_dice_get_number(2)
	
	def check_final_range(self):
		energy_point = 0
		damage_take = 0
		if self.check_full():
			for i in range(0, 4):
				diff = self.board(0, i) - self.board(1, i)
				if diff == 5:
					energy_point = energy_point + 2
				elif diff == 4:
					energy_point = energy_point + 1
				elif diff < 1:
					damage_take = damage_take + 1
		return (energy_point, damage_take)

	def play(self, strategy, energy_point):
		print("Activation started:")
		while not self.check_full():
			numbers = self.roll_dice_get_number()
			print("These are numbers you can put in the board:")
			print(numbers)
			moves = strategy(numbers, self.board)
			self.put_number(moves[0][0], moves[0][1], moves[0][2])
			self.put_number(moves[1][0], moves[1][1], moves[1][2])
			print("This is the current state of the board:")
			print(self.board)
			for i in range(0, 4):
				if self.board[0][i] - self.board(1, i) == 0:
					self.board[0][i] = 0
					self.board[1][i] = 0
					print("difference = 0: reroll")
					numbers = self.roll_dice_get_number()
					print("These are numbers you can put in the board:")
					print(numbers)
					moves = strategy(numbers, self.board)
					self.put_number(moves[0][0], moves[0][1], moves[0][2])
			self.put_number(moves[1][0], moves[1][1], moves[1][2])
		energy_point = energy_point + self.check_final_range()
		if energy_point >= 4:
			return True
		else:
			return False

class Connection(Minigame): #will need to add UtopiaEngine later
	"""A class that simulates the Connection part of the game
		The UtopiaEngine class should check that there are
		sufficient components available before creating an instance
		of this class."""

	def __init__(self):
		game_temp = Minigame(2, 3)
		self.board = game_temp.board
		self.roll = []

	def states(self): 
		"""Returns each state as a set of 3 2x1 arrays."""
		subset = []
		for i in range(1, 7):
			for j in range(1, 7):
				subset.append(np.array([[i], [j]]))
		allstates = list(combinations_with_replacement(subset, 3))
		return allstates

	def possible_actions(self):
		positions = []
		for i in range(3):
			for j in range(3):
				positions.append((i, j))
		unique_moves = []
		for n in range(1, 7):
			for position in positions:
				unique_moves.append(n, position)
		return list(combinations(unique_moves, 2))


	def state2board(self, state):
		return np.hstack((state[0], state[1], state[2]))

	def board2state(self, board):
		return np.hsplit(board, 3)
		
	def roll_dice_get_number():
		self.roll = Minigame.roll_dice_get_number(2)
		return self.roll

	# def toss(self, num):
	# 	if (len(UtopiaEngine.wastebasket) < 10):
	# 		UtopiaEngine.wastebasket.append(num)
	# 		self.roll.remove(num)
	# 		new_num = Minigame.roll_dice_get_number(1)
	# 		self.roll.append(new_num)
	# 	return self.roll

	def play(self, strategy):
		while not check_full():
			result = roll_dice_get_number()
			moves = strategy(result)
			for move in moves:
				num = move[0]
				row = move[1][0]
				col = move[1][1]
				if self.board[row][col] == 0:
					put_number(num, row, col)
				# elif check_full():
				# 	toss(num)
		state = board2state(self.board)
		link = 0
		for pair in state:
			diff = np.subtract(pair[0], pair[1])[0]
			if diff < 0:
				#UtopiaEngine.hitpts -= 1
				decision = strategy() #determines whether to spend another component
				if decision == 'continue':
					link += 2
				else:
					return
			else:
				link += diff
		return link

class Search(Minigame):
	"""Class for search minigame.
	"""
	def __init__(self):
		Minigame.__init__(self, 2, 3)

	def play(self, policy):
		"""Play through one search round. Returns final difference after filling in board.
			Arguments:
				policy: a function that takes in the current state and returns a legal action
		"""
		while not self.check_full():
			print("Current board: ")
			print(self.board)
			roll1, roll2 = self.roll_dice_get_number(2)
			space1, space2 = policy(self)
			self.board[space1] = roll1
			self.board[space2] = roll2

		print("Current board: ")
		print(self.board)
		val1 = self.board[0][0]*100 + self.board[0][1]*10 + self.board[0][2]
		val2 = self.board[1][0]*100 + self.board[1][1]*10 + self.board[1][2]
		print("Your serach result: ", val1-val2)
		return val1 - val2

	def legalActions(self):
		"""Returns list of ways a pair of numbers can be placed on the board.
			If no empty spaces, moves represented as list of form:
				[(row, column) where 1st number goes, (row, column) where 2nd number goes]
		"""
		emptySpaces = []
		for row in range(2):
			for col in range(3):
				if self.board[(row, col)] == 0:
					emptySpaces.append( (row, col) )

		# List of all pairs of spaces with repeats
		# e.g. permutations([1, 2, 3], 2) returns [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
		actions = list(permutations(emptySpaces, 2))
		print("Actions: ", actions)
		return actions
		