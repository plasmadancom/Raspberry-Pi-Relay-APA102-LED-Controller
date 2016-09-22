#!/usr/bin/python

# io.py - Setup GPIO ports
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


# Import dependancies
from config import *
import wiringpi                                              # Source: https://github.com/WiringPi/WiringPi-Python

wiringpi.wiringPiSetup()                                     # Set WiringPi ports. See http://wiringpi.com/pins/

wiringpi.pinMode(button1, 0)                                 # Set button1 to input mode
wiringpi.pullUpDnControl(button1, 2)                         # Set pull-up

wiringpi.pinMode(button2, 0)                                 # Set button2 to input mode
wiringpi.pullUpDnControl(button2, 2)                         # Set pull-up

wiringpi.pinMode(ac_detect_port_1, 0)                        # Set ac_detect_port_1 to input mode
wiringpi.pullUpDnControl(ac_detect_port_1, 1)                # Set pull-down

wiringpi.pinMode(ac_detect_port_2, 0)                        # Set ac_detect_port_2 to input mode
wiringpi.pullUpDnControl(ac_detect_port_2, 1)                # Set pull-down

wiringpi.pinMode(motor_pwr, 1)                               # Set motor_pwr to output mode
wiringpi.pinMode(motor_relay, 1)                             # Set motor_relay to output mode
wiringpi.pinMode(buffer1, 1)                                 # Set buffer1 to output mode
wiringpi.pinMode(buffer2, 1)                                 # Set buffer2 to output mode
wiringpi.pinMode(buffer3, 1)                                 # Set buffer3 to output mode