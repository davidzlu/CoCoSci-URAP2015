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

#def take_action(board, endrow, endcolumn, direction):
#	1 = down 2 = right 3 = up 4 = left
#	assert direction = 1 or direction = 2 or direction = 3 or direction = 4
#	x = board[:][:]
#	x[endrow][endcolumn] = 1
#	if direction = 1:
#		x[endrow + 1][endcolumn] = 0
#		x[endrow + 2][endcolumn] = 0
#	elif direction = 2:
#		x[endrow][endcolumn - 1] = 0
#		x[endrow][endcolumn - 2] = 0
#	elif direction = 3:
#		x[endrow - 1][endcolumn] = 0
#		x[endrow - 2][endcolumn] = 0
#	elif direction = 4:
#		x[endrow][endcolumn + 1] = 0
#		x[endrow][endcolumn + 2] = 0
#	return x
