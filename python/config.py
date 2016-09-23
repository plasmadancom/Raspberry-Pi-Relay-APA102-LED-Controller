#!/usr/bin/python

# config.py - Define all settings / variables for both Python & PHP
# 
# Copyright (C) 2016 Dan Jones - https://plasmadan.com
# 
# Full project details here:
# https://github.com/plasmadancom/Raspberry-Pi-Relay-APA102-LED-Controller
# https://www.avforums.com/threads/ongoing-plasmadans-living-room-cinema-office-build.1992617/
# 
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# -----------------------------------------------------------------------------


# Web GUI language
title = 'Light Controller'                # Web GUI title
relay_ch1_label = 'LEDS'                  # Relay channel 1 label
relay_ch2_label = 'SPOTLIGHTS'            # Relay channel 2 label
motor_label = 'BLIND'                     # Motor control label
preset_label = 'PRESET'                   # Preset button label
reboot_label = 'Reboot'                   # Reboot button label

lang_success = 'Done!'
lang_warning = 'Warning!'
lang_error = 'Error!'
lang_ac_detect_error = 'LED driver not powered!'
lang_ajax_error = 'AJAX response was null or empty!'
lang_ajax_invalid = 'AJAX response was invalid!'
lang_ajax_missing = 'AJAX response is missing data!'
lang_setting = 'Setting'
lang_setting_color = 'Color'
lang_setting_brightness = 'Brightness'
lang_set_color_mismatch = 'Set color did not match requested color! Result'
lang_set_brightness_mismatch = 'Set brightness did not match requested brightness! Result'
lang_switching = 'Switching'
lang_cycling = 'Cycling preset...'
lang_motor_up = 'up...'
lang_motor_down = 'down...'
lang_motor_toggle = 'Toggle motor'
lang_rebooting = 'Rebooting controller...'
lang_rebooting_inprogress = 'Controller reboot in progress...'
lang_rebooting_slow = 'Taking longer than expected...'
lang_rebooting_error = 'Please check the controller!'
lang_rebooting_done = 'Controller online!'
lang_invalid_color_data = 'Incorrect or partially missing color data'
lang_valid_colors = 'Valid color formats'
lang_invalid_file = 'File data invalid, returned length'

# Web GUI settings
enable_relay_ch2 = 1                      # Enable / disable relay channel 2
enable_motor_control = 1                  # Enable / disable motor control
preset_button = 1                         # Add a preset button to web GUI (emulates button1 input)
reboot_button = 1                         # Add a system reboot button to web GUI
autoupdate = 1                            # Enable / disable automatic refreshing of web GUI
refresh_timer = 1000                      # Automatically refresh web GUI (miliseconds)
ajax_timeout = 5000                       # Response timeout for GUI controls, increase if using over the internet (miliseconds)

# AC detection
# Enable for 2-way lighting control
# Wire to L1 if not needed (relay NO)
ac_detect = 1                             # Enable / disable AC detection (I1 / I2 directly, or loop-back from change-over relays)
ac_detect_port_1 = 0                      # I1 AC detection WiringPi port (0 - 1)
ac_detect_port_2 = 1                      # I2 AC detection WiringPi port (0 - 1)

# Motor
button2 = 6                               # Motor control input WiringPi port (6 - 7)
button2_delay = 0.4                       # Prevent accidental double button2 presses with this delay (seconds)
motor_timer = 10                          # Minimum time to complete one FULL blind cycle (seconds)
motor_pwr = 4                             # Main switching relay WiringPi port
motor_relay = 5                           # Changeover relay WiringPi port
motor_direction_delay = 0.2               # Wait before changing motor direction (seconds) - FOR SAFETY!!
motor_direction = 0                       # Starting motor direction (0 or 1) depending on wiring
motor_delay = 0.5                         # Minimum time to run motor (seconds)

# Relays
relay_1 = 3                               # Channel 1 relay WiringPi port
relay_2 = 2                               # Channel 2 relay WiringPi port
buffer_sleep = 50000                      # Time to change buffer status back to off (microseconds)

# Buffer
buffer1 = 17                              # Spare WiringPi ports to use as simple way to communicate between PHP & Python
buffer2 = 18
buffer3 = 19

# LEDs
numpixels = 600                           # Number of LEDs in strip
spi = 7800000                             # SPI interface rate, adjust if LEDs flicker or do not show correctly
rgb_order = 'bgr'                         # Adafruit DotStars (APA102C) use 'bgr', change order to work with different strips
button1 = 7                               # Preset control input WiringPi port (6 - 7)
button1_delay = 0.2                       # Prevent accidental double button1 presses with this delay (seconds)
hold_delay = 0.2                          # Mimimum time to wait before re-checking button1 state
lux_enable = 1                            # Enable / disable brightness cycle. Will cycle colors if disabled. Hold button1 down to cycle
lux_steps = 4                             # Steps to count when creating brightness levels, lower steps means smoother transition (1 - 25)
lux_delay = 0.05                          # Delay when cyclying through brightness levels (seconds)
lux_lowest = 10                           # Lowest permissible brightness level (0 - 255)
lux_highest = 255                         # Highest permissible brightness level (1 - 255)
fade_dir = 0                              # Fade up / down initial direction
save_caching = 0                          # Enable / disable caching of color & brightness to in-memory SQLite database (EXPERIMENTAL)
save_to_file = 1                          # Enable / disable saving of color & brightness to file
savefile = '/var/www/html/color.txt'      # File to save color & brightness level for next boot, needs 755 permissions!
save_off = 1                              # Enable / disable saving of LED off state (this also supercedes lux_lowest)
backup_col = [255, 255, 255, 128]         # Backup if savefile error, list of 4 digits 0 - 255 (Red, Green, Blue, Brightness)

# Transitions / effects
transition_effect = 'fade'                # fade / wipe / 0 (none)
wipe_effects = 0                          # Cannot use color fade when transitioning to / from an effect, use (1) to use wipe instead, or (0) to skip
shift_pixels = 0                          # Shift position of LED 1 for use with transition effects (+/-)
color_fade_steps = 16                     # Steps when fading between colors
color_fade_delay = 0.02                   # Delay between each color fade step (seconds)
rainbow_start = 1                         # Start LED for rainbow effect

# Starting index for preset list
preset_idx = 0

# Preset colors (R/G/B) / effect
# Supports RGB or 24-bit color format
# Don't put two of the same color / effect or you'll mess-up the indexing
preset = [
	'rainbow',                            # RGB color wheel (static)
#	'rainbowrotate',                      # Rotating RGB color wheel (EXPERIMENTAL)
	[255, 255, 255],                      # White
	[255, 0, 0],                          # Pure Red
	[255, 50, 0],                         # Orange
	[255, 255, 0],                        # Yellow
	[0, 255, 0],                          # Green
	[0, 255, 255],                        # Cyan
	[0, 0, 255],                          # Pure Blue
	[16711935]                            # Pink (24-bit example) same as [255, 0, 255]
]
