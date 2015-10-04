import string
digs = string.digits

"""The following code to convert an integer to a string in base x 
is adapted from http://stackoverflow.com/a/2267446
Meant to be the inverse of the built in function int(x, base) where 
x must be a string if a base other than 10 is specified."""
def int2base(x, base):
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

def create_states(boardsize=4):
	total = 3**boardsize
	states = []
	for i in range(0, total+1):
		states.append(int2base(i,3))
	return states

