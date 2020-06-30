from .packet import Packet, Field, SIZE_BOOL, SIZE_INT32
from .net import Protocol


# ----------------------------------------------------------------------------------------------------------------------

class Packet0Data(Packet):
	"""
	A data packet for Assignment 2.
	"""

	ID = 0
	FIELDS = [
		Field(name="Data", size=SIZE_INT32),
		Field(name="SeqSeg", size=SIZE_BOOL),
		Field(name="SeqAck", size=SIZE_BOOL),
		Field(name="Ack", size=SIZE_BOOL)
	]

	def __init__(self):
		super().__init__()
		self.data = 0
		self.sequence_segment = 0
		self.sequence_acknowledgement = 0
		self.acknowledgement = False

	def __str__(self):
		return " data = " + str(self.data) \
				+ "  seqSeg = " + str(self.sequence_segment) \
				+ "  seqAck = " + str(self.sequence_acknowledgement) \
				+ "  isack = " + ("1" if self.acknowledgement else "0")
	
	def as_ack(self):
		"""
		Gets a copy of the packet as an ACK response.
		:return: The response packet.
		"""
		copy = Packet0Data()
		copy.data = self.data
		copy.sequence_segment = 0
		copy.sequence_acknowledgement = self.sequence_segment
		copy.acknowledgement = True
		return copy

	@property
	def data(self):
		return self._raw[0]

	@data.setter
	def data(self, value):
		self._raw[0] = value

	@property
	def sequence_segment(self):
		return self._raw[1]

	@sequence_segment.setter
	def sequence_segment(self, value):
		self._raw[1] = value

	@property
	def sequence_acknowledgement(self):
		return self._raw[2]

	@sequence_acknowledgement.setter
	def sequence_acknowledgement(self, value):
		self._raw[2] = value

	@property
	def acknowledgement(self):
		return self._raw[3] == 1

	@acknowledgement.setter
	def acknowledgement(self, value):
		if type(value) == bool:
			value = 1 if value else 0

		self._raw[3] = value


class Packet1Suicide(Packet):
	"""
	A packet that tells the client or server to exit.
	"""

	ID = 1
	FIELDS = []


# ----------------------------------------------------------------------------------------------------------------------

ASN2_PROTOCOL = Protocol([
	Packet0Data,
	Packet1Suicide
])
