import numpy as np

def create_board():
	board = np.ones((7,7))
	board[0:2, 0:2] = 0
	board[0:2, 5:] = 0
	board[5: , 0:2] = 0
	board[5: , 5: ] = 0
	board[3, 3] = 0
	return board