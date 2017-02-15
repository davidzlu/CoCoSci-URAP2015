import random

class Situation:
	"""Abstract class for situations. Defines instance variables
	and common methods. Most actions involving SO points and
	tracking days will be defined here.
	"""
	
	def __init__(self):
		self.SOpoints = 0
		self.days = 0
		self.dailySO = 0
		self.day = 1
		self.special = None
		
	def get_so_points(self):
		return self.SOpoints
	
	def get_days(self):
		return self.days
		
	def get_daily_so(self):
		return self.dailySO
	
	def get_day(self):
		return self.day
	
	def get_special(self):
		return self.special
		
	def spend_so_points(self, n):
		assert n > 0
		if n <= self.SOpoints:
			self.SOpoints -= n
			return n
		else:
			return 0
		
	

class Surge(Situation):

	def __init__(self):
		self.SOpoints = 30
		self.days = 3
		self.dailySO = 6

		# TODO: encode goal checking for this situation, namely:
		# 1. Destory 8 Battlions on the first day 
		# 2. 4 on the second day.

	