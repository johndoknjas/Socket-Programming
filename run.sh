#!/bin/bash
option() { echo "$2"; }
reset() { { kill "${JOB_SENDER}"; kill "${JOB_RECEIVER}"; } &>/dev/null; }

{ python3 asn2_receiver.py < <(
	option "Corruption Seed"        123
	option "Corruption Probability" 0.5
) & }; sleep 0.2; JOB_RECEIVER=$!

if ! kill -0 "$JOB_RECEIVER" &>/dev/null; then reset; exit 1; fi
{ sleep 0.5; python3 asn2_sender.py < <(
	option "Timing Seed"            111
	option "Segments"               1
	option "Corruption Seed"        456
	option "Corruption Probability" 0.5
	option "Data Seed"              789
	option "RTT Time"               5
) & }; JOB_SENDER=$!
	
trap 'reset' INT
wait "$JOB_SENDER" &>/dev/null
wait "$JOB_RECEIVER" &>/dev/null
reset
