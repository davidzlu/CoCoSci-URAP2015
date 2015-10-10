import string
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
	Returns a list of all possible states represented as bit strings

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

#returns list of all legal possible configurations for a 2x2 board
def state_space():
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
		if (x > 2) or (o > 2) or (x > 1 and o < 1) or (o > 1 and x < 1):
			invalid.append(item)
	for item in invalid:
		states.remove(item)
	return states





# def legal_actions(player, curr_state, states):
# 	laction_set = []
# 	for x in states:
# 		for i in range(4):
# 			if curr_state[i] == 0 or curr_state[i] == player:
# 				if x not in laction_set:
# 					laction_set.append(x)
# 	return laction_set

