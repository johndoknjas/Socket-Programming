from common.net import Client
from common.random import Random
from common.asn2 import ASN2_PROTOCOL, Packet0Data, Packet1Suicide
from common.debug import debug

debug.name = "sender"
debug.enabled = False


class Config:
	def __init__(self):
		self.timing_random = Random()
		self.segments = 5
		self.corruption_random = Random()
		self.corruption_probability = 0.5
		self.data_random = Random()
		self.rtt = 3

	def read_from_stdin(self):
		self.timing_random.seed = input()
		self.segments = int(input())
		self.corruption_random.seed = input()
		self.corruption_probability = float(input())
		self.data_random.seed = input()
		self.rtt = float(input())

	def is_corrupted(self):
		# Paraphrasing from the assignment:
		# > If the number generated is less that the input value of the corruption probability, the packet is to be
		# > considered corrupted.
		#
		# The last_bool function generates `True` if the number is greater than or equal to, so we simply take its
		# inverse to meet that criteria.
		return not self.corruption_random.next_bool(self.corruption_probability)

	def generate_data(self):
		return self.data_random.next_int(0, 1024)

	def generate_delay(self):
		return self.timing_random.next_float(0, 5)
	

def STATE_SEND_PACKET(client):
	# Increment the sequence.
	client.last_sequence += 1
	
	# Exit if the number of segments has been sent is reached.
	if client.last_sequence == config.segments:
		client.send(Packet1Suicide())
		return None
	
	# Create the packet to send.
	packet = Packet0Data()
	packet.data = config.generate_data()
	packet.sequence_segment = client.last_sequence % 2
	client.last_packet = packet
	
	# Send the packet.
	print("A data segment with sequence number " + str(client.last_sequence % 2) + " is about to be sent")
	print("Segment sent: " + str(packet))
	client.send(packet)

	print("The sender is moving to state WAIT FOR ACK " + str(client.last_sequence % 2))
	return STATE_WAIT_FOR_ACK


def STATE_RESEND_PACKET(client):
	print("A data segment with sequence number " + str(client.last_sequence % 2) + " is about to be resent")
	print("Segment sent: " + str(client.last_packet))
	client.send(client.last_packet)

	print("The sender is moving back to state WAIT FOR ACK " + str(client.last_sequence % 2))
	return STATE_WAIT_FOR_ACK


def STATE_WAIT_FOR_ACK(receiver):
	packet = receiver.recv(timeout=config.rtt)

	# Handle timeout.
	if packet is None:
		return STATE_RESEND_PACKET

	# Handle corrupted packets.
	if config.is_corrupted():
		print("A Corrupted ACK segment has just been received")
		
		# FIXME: Ask prof what to do if the sender's ACK is corrupted.
		#        I assume that it's best to pretend it was never received, and re-send it.
		return STATE_RESEND_PACKET

	# Next.
	print("An ACK" + str(packet.sequence_acknowledgement) + " packet has just been received")
	print("ACK received: " + str(packet))
	return STATE_SEND_PACKET




config = Config()
# config.read_from_stdin()
client = Client(ASN2_PROTOCOL)
client.last_sequence = -1
client.last_packet = None

client.start(STATE_SEND_PACKET)