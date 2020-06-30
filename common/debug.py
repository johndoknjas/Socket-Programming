from sys import stderr as __stderr


class DebugPrinter:

	def __init__(self, file):
		self.enabled = False
		self.name = None
		self.__file = file

	def __call__(self, *args, **kwargs):
		"""
		Prints a debug message.
		"""
		if self.enabled:
			name = ""
			if self.name is not None:
				name = ":" + self.name
			print("DEBUG" + name + ">", *args, file=self.__file, **kwargs)


debug = DebugPrinter(__stderr)
