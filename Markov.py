import string
from TicTacToe import *
import random
import numpy as np
digs = string.digits

def int2base(x, base):
	"""Code which converts an integer into a string in base x 
	Adapted from http://stackoverflow.com/a/2267446
	Meant as an inverse of the built in function int(x, base)"""
	if x < 0:
		sign = -1
	elif x == 0:
		return digs[0]
	else:
		sign = 1
	x *= sign
	digits = []
	while x:
		digits.append(digs[x % base])
		x = x//base
	if sign < 0:
		digits.append('-')
	digits.reverse()
	return ''.join(digits)


def create_states(numpieces=3, boardsize=4):
	"""
	Returns a list of all possible states represented as bit strings where
	string indexes correspond to spaces on the board like so:
    0 = [0,0] 1 = [0,1]
    2 = [1,0] 3 = [1,1]

	numpieces: Number of configurations a particular space can take, 
			   including the null configuration.
	boardsize: Number of spaces on the gameboard
	"""
	total = numpieces**boardsize
	states = []
	for i in range(0, total):
		state = int2base(i,numpieces)
		if len(state) < boardsize:
			state = (str(0)*(boardsize - len(state))) + state
		states.append(state)
	return states

def state_space():
	"""Returns a list of all legal states for a 2x2 game of TicTacToe"""
	states = create_states()
	invalid = []
	for item in states:
		x = 0
		o = 0
		#counts numbers of x's and o's to make sure no player skipped another's turn
		for digit in range(4):
			if item[digit] == '1':
				x += 1
			elif item[digit] == '2':
				o += 1
		if (x > o+1) or (o > x+1):
			invalid.append(item)
	for item in invalid:
		states.remove(item)
	return states


def create_state_tree(states):
	""" Takes in list of states as base 3 string of digits.
	Creates dictionary that maps a state to a list of all the ones
	rechable from it."""
	state_tree = {}
	for cur_state in states:
		state_tree[cur_state] = []
		for next_state in states:
			if valid_transition(cur_state, next_state):
				state_tree[cur_state].append(next_state)
	return state_tree


def action_space(board):
    """Returns list of all possible actions for the given board"""
    actions = []
    for i in range(len(board)):
        for j in range(len(board)):
            actions.append([i,j])
    return actions

def legal_actions(curr_state, actions):
    """Returns list of legal moves to make on your turn

    curr_state: bit string representing current game curr_state
    actions: list of all possible actions
    """
    laction_set = []
    for item in actions:
        if curr_state[actions.index(item)] == '0':
            laction_set.append(item)
    return laction_set

def board2state(board):
	"""Returns string representation of the board passed in"""
	s = ''
	for i in board:
		for j in i:
			s += str(j)
	return s

def valid_transition(cur_state, next_state):
	if cur_state == next_state:
		return False
	cur_board = state2board(cur_state)
	if check_win(cur_board)[0]:
		return False
	num_differs = 0
	for i in range(0, len(cur_state)):
		if cur_state[i] != '0' and next_state[i] != cur_state[i]:
			return False
		if cur_state[i] != next_state[i]:
			num_differs += 1
	if num_differs <= 2:
		return True
	return False

def state2board(state, rows=2, columns=2):
	board = []
	for row in range(rows):
		board_row = []
		for col in range(columns):
			board_row.append(int(state[(row*columns) + col]))
		board.append(board_row)
	return board

def transition_prob(next_state, cur_state, action, state_tree):
    """ Return probability of transitioning into next_state from
    cur_state and action. Distribution function method. Should get info from
    policy. """
    if next_state in state_tree[cur_state]:
    	next_level = state_tree[cur_state]
    	possible_states = next_states(cur_state, action, state_tree)
    	num_rechable_states = len(possible_states)
    	vector = [0]*len(next_level)
    	if num_rechable_states > 0:
    		prob =  1.0/num_rechable_states
    		for i in range(len(vector)):
    			if next_level[i] in possible_states:
    				vector[i] = prob
    		return prob, vector
    return 0, np.zeros(len(state_tree[cur_state]))

def transition_prob_matrix(board):
	"""
	Creates a transition probability matrix for the board passed in 
	for which transition_prob_matrix[i, j, k] refers to 
	[current state, next state, action].

	"""
	actions = action_space(board)
	curr_state = board2state(board)
	states = state_space()
	state_tree = create_state_tree(states)
	array_list = []
	for move in actions:
		test_state = simulate_transition(curr_state, move)[0]
		if test_state in state_tree:
			for next_state in state_tree[test_state]:
				if moves_made(next_state) == moves_made(test_state)+1:
					array_list.append(transition_prob(next_state, curr_state, move, state_tree)[1])
					break
			if state_tree[test_state] == []:
				array_list.append(transition_prob(test_state, curr_state, move, state_tree)[1])
		else:
			array_list.append(np.zeros(len(state_tree[curr_state])))
	matrix = np.array(array_list[0])
	for array in array_list[1:]:
		matrix = np.dstack((matrix, np.array(array)))
	return matrix

def next_states(cur_state, action, state_tree):
	""" Return list of next possible states given current and action. """
	states = []
	for state in state_tree[cur_state]:
		space_check = 2*action[0] + action[1]
		if state[space_check] == '1':
			if simulate_transition(cur_state, action)[0] != cur_state:
				if moves_made(state) == moves_made(cur_state)+1:
					if check_win(state2board(state)) == (True, 1):
						states.append(state)
						break
			if moves_made(state) == moves_made(cur_state)+1:
				states.append(state)
	return states

def reward_function(cur_state, action, next_state):
	""" Rewards calculated for each move. Returns 1 for a win,
	-1 for a loss, and -100 for illegal moves. """
	expected_reward = 0
	win, player = check_win(state2board(next_state))
	actions = action_space(state2board(cur_state))
	if win and (cur_state != next_state):
		if player == 1:
			expected_reward = 1
		elif player == 2:
			expected_reward = -1
	if action not in legal_actions(cur_state, actions):
		expected_reward = -100
	return expected_reward


def simulate_transition(cur_state, action):
	""" Returns next state and a corresponding reward. """
	cur_board = state2board(cur_state)
	next_board = put_piece(cur_board, action[0], action[1], 1)
	next_state = board2state(next_board)
	reward = reward_function(cur_state, action, next_state)
	return next_state, reward

if __name__ == "__main__":
	states = state_space()
	state_tree = create_state_tree(states)
	matrix = transition_prob_matrix(create_board())

def opt_avf(cur_state, cur_action, state_tree, d, e):
	if state_tree[cur_state] == []:
		return 0
	value = 0
	while d >= e:
		possible_states = next_states(cur_state, cur_action, state_tree)
		for next_state in possible_states:
			for action in action_space([[0,0],[0,0]]):
				next_value = transition_prob(next_state, cur_state, action, state_tree)[0] * (reward_function(cur_state, action, next_state)
				 + opt_avf(next_state, action, state_tree, d, e))
				value = max(value, next_value)
				d = min(d, abs(value-next_value))
	return value


def q(cur_state, action):
	test_state, reward = simulate_transition(cur_state, action) #first examine if any reward is produced in this action
	test_board = state2board(test_state)
	states = create_states()
	state_tree = create_state_tree(states) #next possible states
	next_rewards = []
	for next_state in state_tree[test_state]:
		trans_prob = transition_prob(next_state, test_state, action, state_tree)[0]
		next_actions = action_space(state2board(next_state))
		rewards = []
		for act in next_actions:
			rewards.append(q(next_state, act)) #append reward of each ection for given possible state
		max_exp_rewards = trans_prob * max(rewards)
		next_rewards.append(max_exp_rewards)
	return reward + sum(next_rewards) #return the reward of this turn and the sum of all possible states according to their transition probability


