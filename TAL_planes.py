import random
from TAL_terrain import *
from TAL_battalions import *
from TAL_situation import *
import unittest

class A_10A:
	def __init__(self):
		self.year = 1976
		self.cannon = 4
		self.so = 8
		self.hit = 3
		"""TODO: weapon list"""
		self.weight = 14

class AH_1:
	def __init__(self):
		self.year = 1967
		self.cannon = 9
		self.so = 2
		self.hit = 1
		"""TODO: weapon list"""
		self.weight = 6

class F_16:
	def __init__(self):
		self.year = 1976
		self.cannon = 7
		self.so = 5
		self.hit = 2
		"""TODO: weapon list"""
		self.weight = 10

class AH_64A:
	def __init__(self):
		self.year = 1986
		self.cannon = 7
		self.so = 4
		self.hit = 2
		"""TODO: weapon list"""
		self.weight = 8

class AV_8B:
	def __init__(self):
		self.year = 1985
		self.cannon = 7
		self.so = 6
		self.hit = 2
		"""TODO: weapon list"""
		self.weight = 10

class A_10C:
	def __init__(self):
		self.year = 2006
		self.cannon = 4
		self.so = 9
		self.hit = 3
		"""TODO: weapon list"""
		self.weight = 14

class MQ_1:
	def __init__(self):
		self.year = 2001
		self.cannon = 0
		self.so = 4
		self.hit = 0
		"""TODO: weapon list"""
		self.weight = 0

class RQ_1:
	def __init__(self):
		self.year = 1995
		self.cannon = 0
		self.so = 4
		self.hit = 0
		"""TODO: weapon list"""
		self.weight = 0

class AH_64D:
	def __init__(self):
		self.year = 1997
		self.cannon = 7
		self.so = 5
		self.hit = 2
		"""TODO: weapon list"""
		self.weight = 8

class AC_130:
	def __init__(self):
		self.year = 1995
		self.cannon = 5 # or 3 or 1
		self.so = 10
		self.hit = 3
		"""TODO: special effect"""
		self.weight = 0

plane_pool = {A_10A: 4, AH_1: 3, F_16: 1, AH_64A: 8, AV_8B: 3, A_10C: 2, MQ_1: 2, RQ_1: 2, AH_64D: 4, AC_130: 1}