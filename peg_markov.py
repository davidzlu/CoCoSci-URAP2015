
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
				actions.append([i, j, 1])
				actions.append([i, j, 2])
				actions.append([i, j, 3])
				actions.append([i, j, 4])
	return actions
