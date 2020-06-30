from random import Random as PyRandom

# ----------------------------------------------------------------------------------------------------------------------

class Random:
	"""
	A seeded random number generator for the Assignment 2 programs.
	"""
	
	def __init__(self, seed=0):
		self.__seed = seed
		self.__rand = PyRandom()
		self.__rand.seed(self.__seed)
	
	@property
	def seed(self):
		return self.__seed
	
	@seed.setter
	def seed(self, value):
		self.__seed = value
		self.__rand.seed(value)
		
	def next_int(self, min, max):
		"""
		Gets the next random integer between min and max.
		:param min: The minimum number possible.
		:param max: The maximum number possible.
		:return: The generated integer.
		"""
		return min + int((max + 1) * self.__rand.random())
	
	def next_float(self, min, max):
		"""
		Gets the next random float between min and max.
		:param min: The minimum number possible.
		:param max: The maximum number possible.
		:return: The generated float.
		"""
		return min + ((max + 1) * self.__rand.random())

	def next_bool(self, probability=0.5):
		"""
		Gets the next random boolean.
		:param probability: The probability of it being true.
		:return: The generated boolean.
		"""
		return self.__rand.random() >= probability

