#!/usr/bin/python

# motor_down.py - Lower the blind / shutter. Meant for use with crontab
# 
# CAUTION!! This script is meant to be used with automatic blind / shutter / projector screen motors with mechanical limits.
# Do not use with the wrong type of motor or you may overwind your motor and damage something!
# You should use the 4-core wired type with 2 x Lives (Up & Down)
# 
# Copyright (C) 2017 Dan Jones - https://plasmadan.com
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
from time import sleep
from config import *
from io import *

try:
    if not wiringpi.digitalRead(motor_pwr):                  # If not running
        wiringpi.pinMode(buffer3, 1)                         # Trigger buffer3
        wiringpi.digitalWrite(buffer3, 1)                    # Write high
        sleep(buffer_sleep)                                  # Delay
        wiringpi.digitalWrite(buffer3, 0)                    # Write low
        sleep(buffer_sleep)                                  # Delay

except Exception as e:                                       # Something went wrong
    print e