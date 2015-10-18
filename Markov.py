import string
from TicTacToe import *
import random
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
	num_differs = 0
	for i in range(0, len(cur_state)):
		if cur_state[i] != '0' and next_state[i] != cur_state[i]:
			return False
		if cur_state[i] != next_state[i]:
			num_differs += 1
	if num_differs == 2:
		return True
	return False

def transition_prob(next_state, cur_state, action, state_tree):
    """ Return probability of transitioning into next_state from
    cur_state and action. """
    if next_state in state_tree[cur_state]:
    	num_rechable_states = 0
    	for state in state_tree[cur_state]:
    		space_check = 2*action[0] + action[1]
    		if state[space_check] == '1':
    			num_rechable_states += 1
    	if num_rechable_states > 0:
    		return 1.0/num_rechable_states
    return 0

def reward_function(cur_state, action, next_state):
	expected_reward = 0
	#if player1 wins, 1 for reward
	#if player2 wins, -1 for reward
	#if neither, 0 for reward
	return None

def simulate_transition():
	""" Simulates a move on the board. """
	#draws a sample from next state and returns associated reward
	return None

	