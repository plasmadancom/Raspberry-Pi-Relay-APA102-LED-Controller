#!/usr/bin/python

# preset.py - Control color & brightness from single push-to-make input
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
from strip import *
from functions import *

ac_status = 0

print 'Preset Button Control Loaded!'

try:
    if ac_detect:
        if off_at_startup:
            if wiringpi.digitalRead(ac_detect_port_1):
                wiringpi.pinMode(relay_1, 1)
                wiringpi.digitalWrite(relay_1, 1)
            
            if wiringpi.digitalRead(ac_detect_port_2):
                wiringpi.pinMode(relay_2, 1)
                wiringpi.digitalWrite(relay_2, 1)
        
        while True:                                          # Loop forever
            if wiringpi.digitalRead(ac_detect_port_1) and not ac_status:
                presshold(1)                                 # Re-initialize strip
                ac_status = 1
            
            if PollPreset():
                if ac_status:
                    presshold()
                
                else:
                    print lang_ac_detect_error
                    
                    sleep(button1_delay)                     # Delay
                    continue
            
            if not wiringpi.digitalRead(ac_detect_port_1) and ac_status:
                SetColor([0, 0, 0])                          # Power down strip
                
                ac_status = 0
    else:
        while True:                                          # Loop forever
            if PollPreset():
                presshold()

except Exception as e:                                       # Something went wrong
    print e

finally:
    SetColor([0, 0, 0])
    #database.close()