from functools import reduce
from math import ceil

# ----------------------------------------------------------------------------------------------------------------------


SIZE_BOOL = 8
SIZE_INT32 = 32


# ----------------------------------------------------------------------------------------------------------------------


class Field:
	"""
	A class representing a field in a packet.
	"""

	def __init__(self, name=None, size=8):
		self.name = name
		self.size = size


class Packet:
	"""
	A class representing a packet.
	"""

	FIELDS = []
	ID = None

	@property
	def FIELDS_SIZE(self):
		return int(ceil(float(reduce(lambda acc, x: acc + x.size, self.FIELDS, 0)) / 8))

	def __init__(self):
		self._raw = []
		for i in range(len(self.FIELDS)):
			self._raw.append(0)


class PacketTranslator:
	"""
	A class that serializes and deserializes packets to/from arrays of bytes.
	"""

	def serialize(self, packet):
		"""
		Serializes a packet into an array of bytes.
		:param packet: The packet to serialize.
		:return: The serialized bytes.
		"""
		buffer = bytearray()
		scratch = 0
		scratch_bits = 0
		for index, data in enumerate(packet._raw):
			field = packet.FIELDS[index]
			bits_remaining = field.size

			while True:
				bits_used = min(8 - scratch_bits, bits_remaining)

				data_to_copy = data >> (bits_remaining - bits_used)
				bits_remaining -= bits_used

				# Copy the bits to the scratch byte.
				scratch <<= bits_used
				scratch |= data_to_copy & ((1 << bits_used) - 1)
				scratch_bits += bits_used

				# Flush the scratch byte to the buffer.
				if scratch_bits == 8:
					buffer.append(scratch)
					scratch = 0
					scratch_bits = 0

				if bits_remaining == 0:
					break

		# Shift over remaining bits and pad.
		if scratch_bits > 0:
			buffer.append(scratch << (8 - scratch_bits))
			
		return buffer

	def deserialize(self, packet, packet_bytes):
		"""
		Deserializes a packet from an array of bytes.
		:param packet: The class of the packet to deserialize.
		:param packet_bytes: The packet bytes to derserialize.
		:return: The deserialized packet.
		"""
		instance = packet()
		current_byte = 0
		current_byte_offset = 0
		for index, field in enumerate(packet.FIELDS):

			bits_required = field.size
			scratch = 0
			scratch_bits = 0
			while True:
				bits_used = min(8 - current_byte_offset, bits_required)
				data_available = packet_bytes[current_byte] & ((1 << (8 - current_byte_offset)) - 1)
				data_to_copy = data_available >> (8 - bits_used - current_byte_offset)

				current_byte_offset += bits_used
				bits_required -= bits_used

				# Copy the data into the scratch byte.
				scratch <<= bits_used
				scratch |= data_to_copy
				scratch_bits += bits_used

				# Choose the next byte from the buffer.
				if current_byte_offset == 8:
					current_byte += 1
					current_byte_offset = 0

				if bits_required == 0:
					instance._raw[index] = scratch
					break

		return instance
