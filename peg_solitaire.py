import numpy as np
import ast
from peg_markov import *
from Game import Game
import random

def create_board():
	"""
	Initializes the standard English peg solitaire game board with 
	the center hole vacant.
	"""
	board = np.ones((7,7))
	board[0:2, 0:2] = 0
	board[0:2, 5:] = 0
	board[5: , 0:2] = 0
	board[5: , 5: ] = 0
	board[3, 3] = 0
	return board.astype(int)

def take_action(board, endrow, endcolumn, direction):
	"""Takes in the board and the target location, where direction is 
	the starting location of the peg relative to the target.
	 1 = down 2 = left 3 = up 4 = right"""
	assert direction == 1 or direction == 2 or direction == 3 or direction == 4
	x = board[:][:]
	x[endrow][endcolumn] = 1
	if direction == 1:
		x[endrow + 1][endcolumn] = 0
		x[endrow + 2][endcolumn] = 0
	elif direction == 2:
		x[endrow][endcolumn - 1] = 0
		x[endrow][endcolumn - 2] = 0
	elif direction == 3:
		x[endrow - 1][endcolumn] = 0
		x[endrow - 2][endcolumn] = 0
	elif direction == 4:
		x[endrow][endcolumn + 1] = 0
		x[endrow][endcolumn + 2] = 0
	return x

def check_win(board):
	"""
	Checks if the player has won or not by counting the number of pegs left.
	Returns True if the game has been won.
	"""
	num_pegs = 0
	for i in range(len(board)):
		for j in range(len(board)):
			if board[i][j] == 1:
				num_pegs += 1
			if num_pegs > 1:
				return False
	if num_pegs == 1:
		return True

def human_player(board):
    """
    A strategy for use with play().
    When passed into play(), an interactive game of Peg Solitaire begins
    This function allows players to input moves into the terminal.
    """
    cur_state = board2state(board)
    moves = legal_actions(board)
    states = next_states(cur_state)
    print("Your available moves are: ")
    print(moves)
    response = input("Enter the move you'd like to make: ")
    my_move = ast.literal_eval(response)
    while my_move not in possible_actions(board):
        my_move = ast.literal_eval(input("Please enter a valid move: "))
    next_state = state_transition(cur_state, my_move)
    expected_reward = reward(cur_state, my_move, next_state)
    print("The result of that move is: ")
    print(state2board(next_state))
    print("Your expected reward for that move is: ")
    print(expected_reward)
    response2 = input("Would you like to change your move? y/n: ")
    if (response2 == 'n') | (response2 == 'no'):
        return my_move
    else:
        return human_player(board)


def play(strategy=human_player):
	"""
	The main function for running a game of PegSolitaire. Default is set to
	human_player phase but this function also accepts any algorithm which returns a move.
	"""
	statesVisited = [] # Sequence of states visited during a game
	actionsTaken = [] # Sequential actions taken during a game
	rewardsGained = [] # Sequence of rewards obtained during a game
	ps = PegSolitaire()
	board = ps.board
	print("The game has begun. The current board state is ")
	print(board)
	while not check_win(board):
		cur_state = board2state(ps.board)
		statesVisited.append(cur_state)
		moves = legal_actions(ps.board)
		move = strategy(ps.board)
		actionsTaken.append(move)
		if move not in moves:
			break
		row, column, direction = move[0], move[1], move[2]
		ps.board = take_action(ps.board, row, column, direction)
		reward = 0
		rewardsGained.append(reward)
		print("The turn has ended. The current board state is ")
		print(board)
	if check_win(ps.board):
		print('The player has won the game!')
		reward = 1
	else:
		print('An illegal move was made. The player has lost the game.')
		reward = -1
	rewardsGained.append(reward)
	return (statesVisited, actionsTaken, rewardsGained, check_win(ps.board))
	
def best_policy(board):
   actions = legal_actions(board)
   curr_state = board2state(board)
   possible_actions_q = {}
   for act in actions:
       key = opt_avf(curr_state, act, 2, 0.5)
       value = key
       entry = act
       possible_actions_q[key] = entry
   best_q = max(possible_actions_q.keys())
   return possible_actions_q[best_q]

#board state 6 jumps from winning: '0000000001000000100000101000001010000010000000000'

def random_policy(board):
    actions = legal_actions(board)
    if len(actions) == 0:
    	return random.choice(possible_actions(board))
    return random.choice(actions)

class PegSolitaire(Game):

	def __init__(self):
		self.board = create_board()

	def possible_actions(self):
		return possible_actions(self.board)

	def random_policy(self):
		return random_policy

	def transition_prob_matrix(self):
		return transition_prob_matrix(self.board)

	def next_states(self):
		state = board2state(self.board)
		return next_states(state)

	def play(self, strategy):
		return play(strategy)

# if __name__ == '__main__':
# 	print('Subclass:', issubclass(PegSolitaire, Game))
