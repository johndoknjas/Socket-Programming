
class StateMachine:
	"""
	A state machine.
	"""

	def __init__(self, receiver):
		self.__state = None
		self.__receiver = receiver

	def start(self, state):
		"""
		Starts the state machine.
		:param state: The initial state.
		"""
		self.__state = state
		while self.__state is not None:
			state = self.__state
			args = []
			
			if type(state) is tuple:
				args = list(state)
				state = args.pop(0)
				
			self.__state = state(self.__receiver, *args)
