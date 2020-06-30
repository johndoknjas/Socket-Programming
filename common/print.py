from sys import stderr as __stderr, modules as __modules

_this = __modules[__name__]


class DebugPrinter:
	"""
	A printer for debug messages.
	"""

	def __init__(self, file):
		self.name = None
		self.__file = file
		self.__enabled = False

	def __call__(self, *args, **kwargs):
		"""
		Prints a debug message.
		"""
		if self.enabled:
			name = ""
			if self.name is not None:
				name = ":" + self.name
			print("DEBUG" + name + ">", *args, file=self.__file, **kwargs)

	@property
	def enabled(self):
		return self.__enabled

	@enabled.setter
	def enabled(self, enabled):
		self.__enabled = enabled
		_this.asnpr = AssignmentFancy() if enabled else AssignmentPrinter()


class AssignmentPrinter:
	"""
	A printer for assignment strings.
	"""

	def corrupted_ack(self):
		print("A Corrupted ACK segment has just been received")

	def corrupted_segment(self):
		print("A Corrupted segment has been received")

	def received_ack(self, packet, duplicate):
		print("ACK received: " + str(packet))

	def received_segment(self, packet, duplicate):
		if duplicate:
			print("A duplicate segment with sequence number " + str(packet.sequence_segment) + " has been received")
		else:
			print("A duplicate segment with sequence number " + str(packet.sequence_segment) + " has been received")

		print("Segment received contains: " + str(packet))

	def sent_ack(self, packet, duplicate):
		print("An ACK" + str(packet.sequence_acknowledgement) + " is about to be sent")
		print("ACK to send contains: " + str(packet))

	def sent_segment(self, packet, duplicate):
		if duplicate:
			print("A data segment with sequence number " + str(packet.sequence_segment) + " is about to be sent")
		else:
			print("A data segment with sequence number " + str(packet.sequence_segment) + " is about to be resent")

		print("Segment sent: " + str(packet))


class AssignmentFancy(AssignmentPrinter):
	"""
	A fancy printer for assignment strings.
	"""

	FANCY_SYM_RECV = "\x1B[32m  <\x1B[0m"
	FANCY_SYM_RECV_DUPLICATE = "\x1B[2;31m* <\x1B[39m"
	FANCY_SYM_SEND = "\x1B[34m  >\x1B[0m"
	FANCY_SYM_SEND_DUPLICATE = "\x1B[2;31m* >\x1B[39m"
	FANCY_SYM_RECV_CORRUPT = "\x1B[31m! <\x1B[39m"
	FANCY_WORD_ACK = "\x1B[33mACK"
	FANCY_WORD_SEG = "\x1B[33mSEG"

	def corrupted_ack(self):
		print(
			AssignmentFancy.FANCY_SYM_RECV_CORRUPT
			+ AssignmentFancy.FANCY_WORD_ACK + "?"
			+ "\x1B[0m: " + "[CORRUPTED]"
		)

	def corrupted_segment(self):
		print(
			AssignmentFancy.FANCY_SYM_RECV_CORRUPT
			+ AssignmentFancy.FANCY_WORD_SEG + "?"
			+ "\x1B[0m: " + "[CORRUPTED]"
		)

	def received_ack(self, packet, duplicate):
		print(
			(AssignmentFancy.FANCY_SYM_RECV if not duplicate else AssignmentFancy.FANCY_SYM_RECV_DUPLICATE)
			+ AssignmentFancy.FANCY_WORD_ACK + str(packet.sequence_acknowledgement)
			+ "\x1B[0m: " + str(packet)
		)

	def received_segment(self, packet, duplicate):
		print(
			(AssignmentFancy.FANCY_SYM_RECV if not duplicate else AssignmentFancy.FANCY_SYM_RECV_DUPLICATE)
			+ AssignmentFancy.FANCY_WORD_SEG + str(packet.sequence_segment)
			+ "\x1B[0m: " + str(packet)
		)

	def sent_ack(self, packet, duplicate):
		print(
			(AssignmentFancy.FANCY_SYM_SEND if not duplicate else AssignmentFancy.FANCY_SYM_SEND_DUPLICATE)
			+ AssignmentFancy.FANCY_WORD_ACK + str(packet.sequence_acknowledgement)
			+ "\x1B[0m: " + str(packet)
		)

	def sent_segment(self, packet, duplicate):
		print(
			(AssignmentFancy.FANCY_SYM_SEND if not duplicate else AssignmentFancy.FANCY_SYM_SEND_DUPLICATE)
			+ AssignmentFancy.FANCY_WORD_SEG + str(packet.sequence_segment)
			+ "\x1B[0m: " + str(packet)
		)


# Assignment printers.
def packet_received(packet):
	if packet.acknowledgement:
		asnpr.received_ack(packet, False)
	else:
		asnpr.received_segment(packet, False)


def packet_received_duplicate(packet):
	if packet.acknowledgement:
		asnpr.received_ack(packet, True)
	else:
		asnpr.received_segment(packet, True)


def packet_received_corrupt(was_ack):
	if was_ack:
		asnpr.corrupted_ack()
	else:
		asnpr.corrupted_segment()


def packet_sent(packet):
	if packet.acknowledgement:
		asnpr.sent_ack(packet, False)
	else:
		asnpr.sent_segment(packet, False)


def packet_sent_duplicate(packet):
	if packet.acknowledgement:
		asnpr.sent_ack(packet, True)
	else:
		asnpr.sent_segment(packet, True)


# Exports.
debug = DebugPrinter(__stderr)
asnpr = AssignmentPrinter()
