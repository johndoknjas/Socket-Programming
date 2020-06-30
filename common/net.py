from .packet import PacketTranslator as _PacketTranslator
from .state import StateMachine as _StateMachine
from .print import debug
import socket as _socket

# ----------------------------------------------------------------------------------------------------------------------

BIND_ADDR = "127.0.0.1"
BIND_PORT = 1378


# ----------------------------------------------------------------------------------------------------------------------


class Protocol:
	"""
	A packet-based network protocol.
	This is used by the Client and Server classes to send different packets over a socket.
	"""

	def __init__(self, packets):
		self._serde = _PacketTranslator()
		self.map = {}
		for packet in packets:
			self.map[packet.ID] = packet

	def get_id(self, packet):
		"""
		Gets the ID of a packet.
		:param packet: The packet object.
		:return: The packet ID.
		"""
		for mapped_id, mapped_packet in self.map.items():
			if mapped_packet.ID == packet.ID:
				return mapped_id
		raise LookupError("Packet type " + type(packet) + " is not mapped.")

	def get_packet(self, id):
		"""
		Gets the Packet subclass of a mapped ID.
		:param id: The packet ID.
		:return: The Packet subclass, or None if not mapped.
		"""
		mapped_packet = self.map.get(id)
		if mapped_packet is not None:
			return mapped_packet
		raise LookupError("Packet ID " + str(id) + " is not mapped.")

	def send_packet(self, connection, packet):
		"""
		Sends a packet over a connection.
		:param connection: The connection to send the packet over.
		:param packet: The packet to send.
		"""
		packet_id = self.get_id(packet)
		packet_bytes = self._serde.serialize(packet)
		packet_data = bytearray([packet_id]) + packet_bytes
		connection.send(packet_data)

	def recv_packet(self, connection, timeout=None):
		"""
		Receives a packet over a connection.
		:param connection: The connection to receive the packet over.
		:param timeout: The timeout.
		:return: None if timed out, or a packet if received successfully.
		"""
		try:
			connection.settimeout(timeout)
			packet_id_buffer = connection.recv(1)
			if len(packet_id_buffer) == 0:
				raise ConnectionAbortedError("The client connection closed.")
			
			packet_id = packet_id_buffer[0]
			packet_class = self.get_packet(packet_id)
			packet_bytes = connection.recv(packet_class().FIELDS_SIZE)
			return self._serde.deserialize(packet_class, packet_bytes)
		except _socket.timeout:
			return None


class __NetCommon:
	def __init__(self):
		self.protocol = None
		self.connection = None
		self.__last_packet = None
		
	def resend(self):
		"""
		Resends the last packet.
		"""
		self.send(self.__last_packet)

	def send(self, packet):
		"""
		Sends a packet.
		:param packet: The packet to send.
		"""
		self.__last_packet = packet
		self.protocol.send_packet(self.connection, packet)

	def recv(self, timeout=None):
		"""
		Receives a packet.
		:param timeout: The packet timeout.
		:return: The packet, or None if it timed out.
		"""
		return self.protocol.recv_packet(self.connection, timeout)


class Client(__NetCommon, _StateMachine):
	def __init__(self, protocol, address=BIND_ADDR, port=BIND_PORT):
		super().__init__()
		_StateMachine.__init__(self, self)
		
		self.protocol = protocol
		self.socket = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
		debug("Establishing a connection...")
		self.socket.connect((address, BIND_PORT))
		self.connection = self.socket
		debug("Established a connection.")


class Server(__NetCommon, _StateMachine):
	def __init__(self, protocol, address=BIND_ADDR, port=BIND_PORT):
		super().__init__()
		_StateMachine.__init__(self, self)
		
		self.protocol = protocol
		self.socket = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
		debug("Waiting for a connection...")
		self.socket.bind((BIND_ADDR, BIND_PORT))
		self.socket.listen(1)
		self.connection, self.remote_addr = self.socket.accept()
		debug("Established a connection.")
