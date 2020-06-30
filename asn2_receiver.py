from common.net import Server
from common.random import Random
from common.asn2 import ASN2_PROTOCOL, Packet1Suicide
from common.debug import debug

debug.name = "receiver"
debug.enabled = False


class Config:
	def __init__(self):
		self.corruption_random = Random()
		self.corruption_probability = 0.5

	def read_from_stdin(self):
		self.corruption_random.seed = input()
		self.corruption_probability = float(input())

	def is_corrupted(self):
		# Paraphrasing from the assignment:
		# > If the pseudo random number is smaller than the probability the segment that has just arrived will be
		# > considered to be corrupted.
		#
		# The next_bool function generates `True` if the number is greater than or equal to, so we simply take its
		# inverse to meet that criteria.
		return not self.corruption_random.next_bool(self.corruption_probability)


def send_ack(server, packet):
	ack = packet.as_ack()
	print("An ACK" + str(packet.sequence_segment) + " is about to be sent")
	print("ACK to send contains: " + str(ack))
	server.send(ack)


def STATE_WAIT_FOR_PACKET(server):
	packet = server.recv(timeout=None)
	if isinstance(packet, Packet1Suicide):
		debug("Receiver told to terminate.")
		exit(0)
	
	# Handle corrupted packets.
	if config.is_corrupted():
		print("A Corrupted segment has been received")
		print("The receiver is moving back to state WAIT FOR " + str(server.next_sequence) + " FROM BELOW")
		return STATE_WAIT_FOR_PACKET
	
	# Handle duplicate packets.
	if packet.sequence_segment == server.last_sequence:
		return STATE_RESPOND_TO_DUPLICATE_PACKET, packet
	
	# Handle good packets.
	return STATE_RESPOND_TO_GOOD_PACKET, packet
	
	
def STATE_RESPOND_TO_GOOD_PACKET(server, packet):
	print("A segment with sequence number " + str(packet.sequence_segment) + " has been received")
	print("Segment received contains: " + str(packet))
	send_ack(server, packet)

	server.next_sequence = (packet.sequence_segment + 1) % 2
	server.last_sequence = packet.sequence_segment
	print("The receiver is moving to state WAIT FOR " + str(server.next_sequence) + " FROM BELOW")
	return STATE_WAIT_FOR_PACKET
	
	
	
def STATE_RESPOND_TO_DUPLICATE_PACKET(server, packet):
	print("A duplicate segment with sequence number " + str(packet.sequence_segment) + " has been received")
	print("Segment received contains: " + str(packet))
	send_ack(server, packet)
	
	print("The receiver is moving back to state WAIT FOR " + str(server.next_sequence) + " FROM BELOW")
	return STATE_WAIT_FOR_PACKET


config = Config()
# config.read_from_stdin()
server = Server(ASN2_PROTOCOL)
server.last_sequence = 1
server.next_sequence = 0

print("The receiver is moving back to state WAIT FOR " + str(server.next_sequence) + " FROM BELOW")
server.start(STATE_WAIT_FOR_PACKET)
