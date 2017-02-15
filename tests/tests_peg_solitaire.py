from peg_markov import *
from peg_solitaire import *
import numpy as np

def reward_test1():
	cur_state = np.zeros((7,7)).astype(int)
	cur_state[(0,2)] = 1
	cur_state[(0,3)] = 1
	cur_state = board2state(cur_state)
	next_state = np.zeros((7,7)).astype(int)
	next_state[(0, 4)] = 1
	next_state = board2state(next_state)
	retval = reward(cur_state, (0, 4, 2), next_state)
	return retval

def reward_test2():
	cur_state = np.zeros((7,7)).astype(int)
	cur_state[(0,2)] = 1
	cur_state = board2state(cur_state)
	next_state = np.zeros((7,7)).astype(int)
	next_state[(0, 3)] = 1
	next_state = board2state(next_state)
	retval = reward(cur_state, (0, 4, 2), next_state)
	return retval

def reward_test3():
	cur_state = create_board()
	cur_state = board2state(cur_state)
	next_state = create_board()
	next_state = take_action(next_state, 3, 3, 2)
	next_state = board2state(next_state)
	retval = reward(cur_state, (3, 3, 2), next_state)
	return retval

def legal_act_test1():
	cur_board = np.zeros((7,7)).astype(int)
	legal_moves = legal_actions(cur_board)
	return legal_moves

if __name__ == '__main__':
	vals1 = reward_test1()
	if vals1 != 1:
		print "reward_test1 failed."
		print "Error: return value doesn't match expected"
		print "Expected 1, got", vals1

	vals2 = reward_test2()
	if vals2 != -1:
		print "reward_test2 failed."
		print "Error: return value doesn't match expected"
		print "Expected -1, got", vals2
		
	vals3 = reward_test3()
	if vals3 != 0:
		print "reward_test3 failed."
		print "Error: return value doesn't match expected"
		print "Expected 0, got", vals2

	moves1 = legal_act_test1()
	if moves1 != []:
		print "legal_act_test1 failed."
		print "Error: return value doesn't match expected"
		print "Expected [], got", vals2