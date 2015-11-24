import numpy as np
from peg_solitaire import *

illegal_spaces = [(0, 0), (1, 0), (5, 0), (6, 0), (0, 1), (1, 1), (5, 1), (6, 1), (0, 5), (0, 6), (1, 5), (1, 6), (5, 5), (5, 6), (6, 5), (6, 6)]


def board2state(board):
	state = ''
	for row in range(len(board)):
		state += ''.join(map(str, board[row, :]))
	return state

def state2board(state):
	board = np.zeros(49).astype(int)
	for i in range(len(state)):
		board[i] = state[i]
	return board.reshape((7,7))

lose_state = board2state(np.zeros((7,7)).astype(int))

def next_states(state):
	states = []
	board = state2board(state)
	for i in range(len(board)):
		for j in range(len(board)):
			if board[(i, j)] == 0:
				if (i, j) not in illegal_spaces:
					#start checking viable directions
					if (i-2 >= 0) and (board[(i-2, j)] == 1) and (board[(i-1, j)] == 1): #up
						states.append(board2state(take_action(board.copy(), i, j, 3)))
					if (i+2 < 7) and (board[(i+2, j)] == 1) and (board[(i+2, j)] == 1): #down
						states.append(board2state(take_action(board.copy(), i, j, 1)))
					if (j-2 >=0) and (board[(i, j-2)] ==1) and (board[(i, j-1)] == 1): #left
						states.append(board2state(take_action(board.copy(), i, j, 2))) 
					if (j+2 < 7) and (board[(i, j+2)] == 1) and (board[(i, j+1)] == 1): #right
						states.append(board2state(take_action(board.copy(), i, j, 4)))
	return states

def possible_actions(board):
	actions = []
	for i in range(len(board)):
		for j in range(len(board)):
			if board[i][j] == 0:
				actions.append((i, j, 1))
				actions.append((i, j, 2))
				actions.append((i, j, 3))
				actions.append((i, j, 4))
	return actions

def legal_actions(board):
	"""
	Returns list of legal actions that can be taken in board.
	"""
	def space_check(space):
		"""
		Helper method for legal_actions. Returns list of legal actions
		that can be taken using space (i, j) as destination.
		"""
		i = space[0]
		j = space[1]
		spaces = []
		if i-2 >= 0: # up
			if board[(i-2, j)] == 1 and board[(i-1, j)] == 1:
				spaces.append((i, j, 3))
		if j-2 >= 0: # left
			if board[(i, j-2)] == 1 and board[(i, j-1)] == 1:
				spaces.append((i, j, 2))
		if i+2 < 7: # down
			if board[(i+2, j)] == 1 and board[(i+2, j)] == 1:
				spaces.append((i, j, 1))
		if j+2 < 7: # right
			if board[(i, j+2)] == 1 and board[(i, j+2)] == 1:
				spaces.append((i, j, 4))
		return spaces

	legal_moves = []
	for i in range(len(board)):
		for j in range(len(board)):
			space = (i, j)
			if space not in illegal_spaces and board[space] == 0:
				legal_moves += space_check(space)
	return legal_moves

def state_transition(state, action):
	""" 
	Returns state agent would enter if takes action in state.
	If no legal actions in state, or if action is not legal,
	return lose state.
	"""
	legal_moves = legal_actions(state2board(state))
	if legal_moves == [] or action not in legal_moves:
		return lose_state
	return board2state(take_action(state2board(state), action[0], action[1], action[2]))

def transition_prob(next_state, cur_state, action):
	moves = legal_actions(state2board(cur_state))
	if action in moves:
		if state_transition(cur_state, action) == next_state:
			return 1
	return 0

def transition_prob_matrix(board):
	actions = possible_actions(board)
	cur_state = board2state(board)
	states = next_states(cur_state)
	array_list = []
	for move in actions:
		test_state = state_transition(cur_state, move)
		if test_state in states:
			array_list.append(transition_prob(test_state, cur_state, move))
		else:
			array_list.append(0)
	matrix = np.array(array_list[0])
	for array in array_list[1:]:
		matrix = np.dstack((matrix, np.array(array)))
	return matrix


def reward(state, action, next_state):
	"""
	Returns 1 if taking action in state is legal, state transitions
	to next_state using action, and next_state is a win state.
	Returns -100 if taking action in state is not legal, or state
	does not transition to next_state using action. Return 0 otherwise.
	"""
	if state_transition(state, action) == next_state:
		if check_win(state2board(next_state)):
			return 1
		elif next_state != lose_state:
			return 0
	return -1

#def legal_actions(board, actions):
#	legal_acts = []
#	for acts in actions:
#		if (acts[0], acts[1]) not in illegal_spaces:
#			try:
#				if acts[2] == 1:
#					if board[acts[0] + 1][acts[1]] = 1 and board[acts[0] + 2][acts[1]] = 1:
#						legal_acts.append(acts)
#				elif acts[2] == 2:
#					if board[acts[0]][acts[1] - 1] = 1 and board[acts[0]][acts[1] - 2] = 1:
#						legal_acts.append(acts)
#				elif acts[2] == 3:
#					if board[acts[0] - 1][acts[1]] = 1 and board[acts[0] - 2][acts[1]] = 1:
#						legal_acts.append(acts)
#				elif acts[2] == 2:
#					if board[acts[0]][acts[1] + 1] = 1 and board[acts[0]][acts[1] + 2] = 1:
#						legal_acts.append(acts)
#			except IndexError as error:
#				pass
#	return legal_acts
