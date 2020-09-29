#!/usr/bin/env python
import PCA9685 as servo
import time                  # Import necessary modules
import sys

CHANNELS = [0, 14, 15]
test_chan = CHANNELS[0]

MinPulse = 0
MaxPulse = 4095

pwm = servo.PWM()
while True:
	line = sys.stdin.readline()
	value = int(line)
	if value >= 0 and value < 4096:
		print "writing", value
		pwm.write(test_chan, 0, value)
	else:
		print "bad value", value

