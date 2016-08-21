#!/usr/bin/python

# motor.py - Blind control from single push-to-make
# CAUTION!! This script is meant to be used with automatic blind / shutter motors with mechanical limits.
# Do not use with the wrong type of motor or you may overwind your blind and damage something!
# You should use the 4-core cabled type with 2 x Lives (Up & Down)
# 
# By Dan Jones - https://plasmadan.com
# 
# Full project details here:
# https://www.avforums.com/threads/ongoing-plasmadans-living-room-cinema-office-build.1992617/

# CONFIG
timer = 10				# Minimum time to complete one FULL blind cycle (seconds)
button = 6				# Button input WiringPi port
motor_pwr = 4			# Main switching relay WiringPi port
motor_relay = 5			# Changeover relay WiringPi port
relay_delay = 0.2		# Wait before changing motor direction (seconds) - FOR SAFETY!!
direction = 0			# Starting motor direction (0 or 1) depending on wiring
button_delay = 0.4		# Prevent accidental double button presses with this delay (seconds)
motor_delay = 0.5		# Minimum time to run motor (seconds)
buffer1 = 17			# Spare WiringPi port to use as simple way to communicate between PHP & Python
buffer2 = 18			# Spare WiringPi port to use as simple way to communicate between PHP & Python


# Import dependancies
import wiringpi
from time import sleep

wiringpi.wiringPiSetup()								# Set WiringPi ports. See http://wiringpi.com/pins/

wiringpi.pinMode(button,0)								# Set button to input mode
wiringpi.pullUpDnControl(button,2)						# Set pull-up

def outputs(mode=1):
	ports = [buffer1, buffer2, motor_pwr, motor_relay]
	
	for port in ports:
		wiringpi.pinMode(port,mode)
		wiringpi.digitalWrite(port,0)

outputs()												# Set WiringPi ports to output mode

def stop():
	global direction
	
	wiringpi.digitalWrite(motor_pwr,0)					# Stop motor_pwr
	wiringpi.digitalWrite(motor_relay,0)				# Stop motor_relay
	
	direction = not direction							# Swap motor direction

def presshold():
	if not wiringpi.digitalRead(button):				# Still pressing! Don't use timer
		while not wiringpi.digitalRead(button):			# Re-check...
			sleep(0.05)
	
	else:												# Use timer
		for i in range(timer*20):
			sleep(0.05)
			
			if not wiringpi.digitalRead(button) or wiringpi.digitalRead(buffer1) or wiringpi.digitalRead(buffer2):
				break									# Interrupt timer

def start(relay=0):
	if relay:
		wiringpi.digitalWrite(motor_relay, 1)			# Start motor_relay
		sleep(relay_delay)								# Wait for relay
	
	wiringpi.digitalWrite(motor_pwr, 1)					# Start motor_pwr
	sleep(motor_delay)
	
	presshold()											# Use timer?
	stop()												# Stop & swap motor direction

print 'Motor Controller Loaded!'

try:
	while True:											# Loop forever
		if not wiringpi.digitalRead(button):			# If button is pressed
			if wiringpi.digitalRead(motor_pwr):			# Already running? (Maybe the web GUI triggered it)
				stop()
			
			elif direction:
				start(1)
			
			else:
				start()
			
			sleep(button_delay)							# Delay
		
		elif wiringpi.digitalRead(buffer1):				# If buffer1 is triggered (by the web GUI)
			if wiringpi.digitalRead(motor_pwr):			# Already running? (Maybe the button triggered it)
				stop()
			
			else:
				start()
			
			sleep(button_delay)							# Delay
		
		elif wiringpi.digitalRead(buffer2):				# If buffer2 is triggered (by the web GUI)
			if wiringpi.digitalRead(motor_pwr):			# Already running? (Maybe the button triggered it)
				stop()
			
			else:
				start(1)
			
			sleep(button_delay)							# Delay

finally:
    outputs(0)											# Reset WiringPi ports to input mode
