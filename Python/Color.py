#!/usr/bin/python

# Color.py - Control color & brightness from single push-to-make
# 
# By Dan Jones - https://plasmadan.com
# 
# Full project details here:
# https://www.avforums.com/threads/ongoing-plasmadans-living-room-cinema-office-build.1992617/

# CONFIG
numpixels = 300												# Number of LEDs in strip
button = 7													# Button input WiringPi port (6 - 7)
button_delay = 0.2											# Prevent accidental double button presses with this delay (seconds)
hold_delay = 0.2											# Mimimum time to wait before re-checking button state
ac_detect = 1												# Enable / disable AC detection (if you're using an LED driver, AC must be connected to I1 or I2)
ac_detect_port = 0											# AC detection circuit WiringPi port (0 - 1)
lux_enable = 1												# Enable / disable brightness cycle. Will cycle colors if disabled. Hold button down to cycle
lux_steps = 4												# Steps to count when creating brightness levels, lower steps means smoother transition (1 - 25)
lux_delay = 0.05											# Delay when cyclying through brightness levels (seconds)
lux_lowest = 5												# Lowest permissible brightness level (0 - 255)
color_fade = 1												# Enable / disable color fading effect
color_fade_steps = 10										# Steps when fading between colors
color_fade_delay = 0.05										# Delay between each color fade step (seconds)
print_on_load = 'Colorpicker Loaded!'						# Print if script loads successfully
savefile = '/var/www/html/color.txt'						# File to save RGB color & brightness level for reference
backup_col = [255,255,255,128]								# Backup if savefile error, list of 4 digits 0 - 255 (Red, Green, Blue, Brightness)

# Preset colors (R/G/B)
white = [255, 255, 255]
red = [255, 0, 0]
orange = [255, 50, 0]
yellow = [255, 255, 0]
green = [0, 255, 0]
cyan = [0, 255, 255]
blue = [0, 0, 255]
pink = [255, 0, 255]

# Array of preset colors
# Makes it easier to re-order them by name
preset = [white,red,orange,yellow,green,cyan,blue,pink]


# Import dependancies
from bisect import bisect_left
from time import sleep

import wiringpi												# Source: https://github.com/WiringPi/WiringPi-Python

from dotstar import Adafruit_DotStar						# Must be in same directory. Source: https://learn.adafruit.com/adafruit-dotstar-leds


wiringpi.wiringPiSetup()									# Set WiringPi ports. See http://wiringpi.com/pins/

wiringpi.pinMode(button, 0)									# Set button to input mode
wiringpi.pullUpDnControl(button, 1)							# Set pull-down

wiringpi.pinMode(ac_detect_port, 0)							# Set button to input mode
wiringpi.pullUpDnControl(ac_detect_port, 1)					# Set pull-down

strip = Adafruit_DotStar(numpixels)							# Declare strip. See https://learn.adafruit.com/adafruit-dotstar-leds

strip.begin()												# Initialize pins for output
strip.show()												# Clear all pixels

c_index = 0													# Index of starting color
sel_c = preset[c_index]										# Select color from array

def GetColor():
	col = backup_col
	
	try:
		with open(savefile, 'r') as f:						# Get color & lux from file
			f.seek(0,0)
			fo = f.readline()
		
		fo_col = fo.split(',')								# Convert text to array
	
	except Exception:										# Something went wrong
		print "Error: Could not open file %s" % savefile
		pass												# Nevermind, use backup instead
	
	if len(fo_col) != 4:									# That's not right!
		print "Error: %s does not contain valid color data! Defaulting to backup." % savefile
	
	else:
		col = fo_col										# Looks good
	
	r = int(col[0])											# Red
	g = int(col[1])											# Green
	b = int(col[2])											# Blue
	l = int(col[3])											# Lux
	
	return [r,g,b,l]										# Return list

def SaveCol(r,g,b,l):
	if r == 0 and g == 0 and b == 0:						# Don't save off state to file, use existing color
		col = GetColor()
		r = col[0]
		g = col[1]
		b = col[2]
	
	if l < lux_lowest:										# Too dim, don't save this brightness level
		col = GetColor()
		l = col[3]
	
	try:
		with open(savefile, 'wb') as f:						# Save new color & lux to text file
			f.write(str(r) + ',' + str(g) + ',' + str(b) + ',' + str(l))
	
	except Exception:										# Something went wrong
		print "Error: Could not write to file %s" % savefile
		pass												# Pass anyway, since we can always use the backup

def SetColor(c):
	col = GetColor()
	
	strip.begin()											# Initialize pins for output
	strip.setBrightness(col[3])								# Set lux level
	
	color = strip.Color(c[1], c[0], c[2])					# Convert color to 24-bit (G/R/B)
	
	for i in range(0,numpixels-1):							# Set each pixel color
		strip.setPixelColor(i,color)
	
	strip.show()											# Light up the strip
	
	SaveCol(c[0],c[1],c[2],col[3])

def calculateFade(old,new):
	step_val = (old - new) / color_fade_steps;				# Divide color transition into step values
	
	list = []												# Create empty list
	
	for i in range(0,color_fade_steps):
		b = int(round(old - (step_val * i)))				# Round each value to whole
		
		if b > 255:
			b = 255											# Limit max
		
		elif b < 0:
			b = 0											# Limit min
		
		list.append(b)										# Add to list
	
	return list												# Return list

def ColorFade(c):
	col = GetColor()
	
	rn = calculateFade(c[0], col[0])						# Get red color transitions
	gn = calculateFade(c[1], col[1])						# Get green color transitions
	bn = calculateFade(c[2], col[2])						# Get blue color transitions
	
	for key, val in reversed(list(enumerate(rn))):
		strip.begin()										# Initialize pins for output
		strip.setBrightness(col[3])							# Set lux level
		
		color = strip.Color(gn[key], val, bn[key])			# Convert color to 24-bit (G/R/B)
		
		for i in range(0,numpixels-1):						# Set each pixel color
			strip.setPixelColor(i,color)
		
		strip.show()										# Light up the strip
		sleep(color_fade_delay)
	
	SaveCol(c[0],c[1],c[2],col[3])

def takeClosest(li, num):
	pos = bisect_left(li, num)								# Find leftmost item greater than or equal to num
	if pos == 0:											# Start of list
		return li[0]
	
	if pos == len(li):										# End of list
		return li[-1]
	
	before = li[pos - 1]
	after = li[pos]
	
	if after - num < num - before:							# Return the smallest num
		return after
	else:
		return before

def FadeInOut(r,g,b,l):
	strip.begin()											# Initialize pins for output
	strip.setBrightness(l)									# Set lux level
	
	color = strip.Color(g, r, b)							# Convert color to 24-bit (G/R/B)
	
	for i in range(0,numpixels-1):							# Set each pixel color
		strip.setPixelColor(i,color)
	
	strip.show()											# Light up the strip

def presshold(shift=1,pwr_cycle=0):
	global c_index,sel_c
	
	sleep(hold_delay)										# Delay
	
	if lux_enable and wiringpi.digitalRead(button):			# Still pressing? Adjust brightness!
		col = GetColor()
		
		lux = []											# Create array of lux levels to use
		l_index = 0											# Default index
		
		start_lux = 0 if pwr_cycle else lux_lowest			# Allows override of lux_lowest when powering up/down the strip
		
		for i in range(start_lux, 255, lux_steps):			# Count up to limit and append values
			lux.append(i)
		
		for i in range(-255, -start_lux, lux_steps):		# Count up from -limit and append absolute values
			lux.append(abs(i))
		
		closest = takeClosest(lux, col[3])
		
		try:
			l_index = lux.index(closest)					# Get index closest to current lux level
		except Exception:
			pass											# Failed. Nevermind, with use default instead
		
		lf = lux[l_index]									# Select the lux from array
		
		while wiringpi.digitalRead(button):					# Re-check...
			FadeInOut(col[0],col[1],col[2],lf)				# Fade in & out
			
			l_index = (l_index + 1) % len(lux)				# Iterate through array of lux levels, then reset
			lf = lux[l_index]
			
			sleep(lux_delay)								# Delay
		
		SaveCol(col[0],col[1],col[2],lf)
		
	
	else:
		if pwr_cycle:
			sel_c = GetColor()								# Load color from file
		
		elif shift:
			c_index = (c_index + 1) % len(preset)			# Shift color index by 1
			sel_c = preset[c_index]							# Select color index from list
		
		if color_fade:
			ColorFade(sel_c)
		
		else:
			SetColor(sel_c)
	
	sleep(button_delay)										# Delay

ac_status = 0

print print_on_load

try:
	if ac_detect:
		while True:											# Loop forever
			if wiringpi.digitalRead(ac_detect_port) and not ac_status:
				presshold(0,1)								# Re-initialize strip
				ac_status = 1
				
			if wiringpi.digitalRead(button):				# If button is pressed
				if ac_status:
					presshold()
				
				else:
					print 'Error: LED driver not powered!'
					
					sleep(button_delay)						# Delay
					continue
			
			if not wiringpi.digitalRead(ac_detect_port) and ac_status:
				SetColor([0,0,0])							# Power down strip
				
				ac_status = 0
	else:
		while True:											# Loop forever
			if wiringpi.digitalRead(button):				# If button is pressed
				presshold()

finally:
	SetColor([0,0,0])
