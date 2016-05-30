import random
import numpy as np
import ast
from copy import deepcopy
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

	def transition_prob_vector(self, action):
		""" Method for finding transition probabilities of all next states
		given current state (self) and an action. Must be overwritten by
		child classes.
		"""
		return

	def next_states(self, action):
		""" Returns all possible next states given current state and an action.
		Must be overwritten by child class.
		"""
		return

	def transition_prob(self, action, next_state):
		""" Returns pobability of transitioning from current state to
		next_state by taking action.  Must be overwritten by child class.
		"""
        # nextPossible = self.next_states(action)
        # if nextState in nextPossible:
        #     return 1.0/float(len(nextPossible))
        # return 0.0
        return

	def legalActions(self, numrows, numcols):
		"""Returns list of ways a pair of numbers can be placed on the board.
			If no empty spaces, moves represented as list of form:
				[(row, column) where 1st number goes, (row, column) where 2nd number goes]
		"""
		emptySpaces = []
		for row in range(numrows):
			for col in range(numcols):
				if self.board[(row, col)] == 0:
					emptySpaces.append( (row, col) )

		# List of all pairs of spaces with repeats
		# e.g. permutations([1, 2, 3], 2) returns [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
		actions = list(permutations(emptySpaces, 2))
		print("Actions: ", actions)
		return actions


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

	def transition_prob_vector(self, action):
		return

	def next_states(self, action):
		return

	def transition_prob(self, action, next_state):
		return

	def play(self, strategy, energy_point):
		print("Activation started:")
		while not self.check_full():
			numbers = self.roll_dice_get_number()
			print("These are numbers you can put in the board:")
			print(numbers)
			moves = strategy(self.legalActions(2, 4), True)
			self.put_number(numbers[0], moves[0][0], moves[0][1])
			self.put_number(numbers[1], moves[1][0], moves[1][1])
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
					moves = strategy(self.legalActions(2, 4), True)
					self.put_number(numbers[0], moves[0][0], moves[0][1])
			self.put_number(numbers[1], moves[1][0], moves[1][1])
		damage_taken = self.check_final_range[1]
		energy_point = energy_point + self.check_final_range()[0]
		if energy_point % 100 >= 4:
			return 999, damage_taken
		else:
			return energy_point, damage_taken

class Connection(Minigame): 
	"""A class that simulates the Connection part of the game
		The UtopiaEngine class should check that there are
		sufficient components available before creating an instance
		of this class."""

	def __init__(self, gamestate):
		game_temp = Minigame(2, 3)
		self.board = game_temp.board
		self.roll = []
		self.gamestate = gamestate #the bigger board

	def transition_prob_vector(self, action):
		return

	def next_states(self, action):
		return

	def transition_prob(self, action, next_state):
		return

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
		
	def roll_dice_get_number(self):
		self.roll = Minigame.roll_dice_get_number(2)
		return self.roll

	def toss(self, num):
		if (len(gamestate.wastebasket) < 10):
			gamestate.wastebasket.append(num)
			self.roll.remove(num)
			new_num = Minigame.roll_dice_get_number(1)
			self.roll.append(new_num)
		return self.roll

	def play(self, strategy):
		while not check_full():
			result = self.roll_dice_get_number()
			for number in result:
				decision = strategy(['keep', 'toss'])
				if decision is 'toss':
					self.toss(number)
			moves = strategy(self.legalActions(2, 3), True)
			for move in moves:
				num = strategy(result)
				result.remove(num) #prevents the number from being used again
				row = move[0]
				col = move[1]
		state = board2state(self.board)
		link = 0
		for pair in state:
			diff = np.subtract(pair[0], pair[1])[0]
			if diff < 0:
				gamestate.hit -= 1
				decision = strategy(['continue', 'stop']) #determines whether to spend another component
				if decision == 'continue':
					link += 2
				else:
					return -1
			else:
				link += diff
		return link

class Search(Minigame):
	"""Class for search minigame.
	"""
	def __init__(self):
		Minigame.__init__(self, 2, 3)
		self.roll1 = 0
		self.roll2 = 0

	def play(self, policy):
		"""Play through one search round. Returns final difference after filling in board.
			Arguments:
				policy: a function that takes in the current state and returns a legal action
		"""
		while not self.check_full():
			print("Current board: ")
			print(self.board)
			self.roll1, self.roll2 = self.roll_dice_get_number(2)
			self = self.simulate_action(policy(self.legalActions(), True))

		print("Current board: ")
		print(self.board)
		val1 = self.board[0][0]*100 + self.board[0][1]*10 + self.board[0][2]
		val2 = self.board[1][0]*100 + self.board[1][1]*10 + self.board[1][2]
		print("Your search result: ", val1-val2)
		return val1 - val2

	def simulate_action(self, action):
		"""Takes in a legal action and returns a copy of the state after taking that action.
		   Does not change current state.
		"""
		next_state = deepcopy(self)
		next_state.board[action[0]] = self.roll1
		next_state.board[action[1]] = self.roll2
		return next_state
	
	def legalActions(self):
		return self.legalActions(2, 3)

	def next_states(self, action):
		"""Returns list of next possible states given current state and action.
		"""
		states = []
		possible_state = deepcopy(self)
		if action in self.legalActions():
			for possible_state.roll1 in range(1, 7):
				for possible_state.roll2 in range(1, 7):
					states.append( possible_state.simulate_action(action) )
		return states

	def transition_prob_vector(self, action):
		return

	def transition_prob(self, action, next_state):
		return


class FinalActivation(Minigame):

	def __init__(self, finalActivationDifficulty):
		self.actNum = finalActivationNumber

	def play(self, policy):
		playerSum = np.sum(roll_dice(2))
		if playerSum >= self.actNum:
			return True
		else:
			return False

	def transition_prob_vector(self, action):
		return

	def next_states(self, action):
		return
