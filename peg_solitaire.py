import numpy as np
from peg_markov import *

def create_board():
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
	num_pegs = 0
	for i in range(len(board)):
		for j in range(len(board)):
			if board[i][j] == 1:
				num_pegs += 1
			if num_pegs > 1:
				return False
	if num_pegs == 1:
		return True

def play(strategy):
	board = create_board()
	print("The game has begun. The current board state is ")
	print(board)
	while not check_win(board):
		cur_state = board2state(board)
		moves = legal_actions(board)
		move = strategy(board)
		if move not in moves:
			break
		row, column, direction = move[0], move[1], move[2]
		board = take_action(board, row, column, direction)
		reward = 0
		print("The turn has ended.The current board state is ")
		print(board)
	if check_win(board):
		print('The player has won the game!')
		reward = 1
	else:
		print('An illegal move was made.')
		reward = -1
	return board, reward