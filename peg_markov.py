
import numpy as np
from peg_solitaire import *


illegal_spaces = [0, 1, 5, 6, 7, 8, 35, 36, 40, 41, 42, 43, 47, 48]

def board2state(board):
	state = ''
	for row in range(len(board)):
		state += ''.join(map(str, board[row, :]))
	return state


