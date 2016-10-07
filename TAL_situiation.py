import random
from TAL_terrain import *
from TAL_campaigns import *



class Surge:

	def __init__(self):
		self.SOpoints = 30
		self.days = 3
		self.dailySO = 6

		# TODO: encode goal checking for this situation, namely:
		# 1. Destory 8 Battlions on the first day  
		# 2. 4 on the second day.