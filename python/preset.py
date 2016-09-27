#!/usr/bin/python

# preset.py - Control color & brightness from single push-to-make input
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
from time import sleep

from config import *
from io import *
from strip import *
from functions import *

def presshold(pwr_cycle=0):
    global fade_dir
    
    sleep(hold_delay)                                        # Delay
    
    if lux_enable and not wiringpi.digitalRead(button1):     # Still pressing? Adjust brightness!        
        col = GetColor()
        
        lux = []                                             # Create array of brightness levels to use
        l_index = 0                                          # Default index
        
        start_lux = 0 if pwr_cycle else lux_lowest           # Allows override of lux_lowest when powering up/down the strip
        
        for i in range(start_lux, lux_highest, lux_steps):   # Count up to limit and append values
            lux.append(i)
        
        for i in range(-lux_highest, -start_lux, lux_steps): # Count up from -limit and append absolute values
            lux.append(abs(i))
        
        closest = takeClosest(lux, col[-1])
        
        try:
            l_index = lux.index(closest)                     # Get index closest to current brightness level
        
        except Exception:
            pass                                             # Failed. Nevermind, with use default instead
        
        lf = lux[l_index]                                    # Select the brightness from array
        
        pixel_cache = CachePixels(col)
        
        while not wiringpi.digitalRead(button1):             # Re-check...
            SetPixels(pixel_cache, lf, 1)                    # Set colour / brightness of each pixel
            
            op = (l_index + 1) if fade_dir else (l_index - 1)
            
            l_index = op % len(lux)                          # Iterate through array of brightness levels, then reset
            lf = lux[l_index]
            
            sleep(lux_delay)                                 # Delay
        
        fade_dir = not fade_dir
        col[-1] = lf
        
        SaveCol(col)
        
        idxs = GetPresetIndex()
        curr_mode = preset[idxs[0]]                          # Select preset index from list
        
        if curr_mode == 'rainbowrotate':                     # Continue rotate
            RainbowRotate(1)
    
    else:
        cyclePreset(pwr_cycle)
    
    sleep(button1_delay)                                     # Delay

ac_status = 0

print 'Preset Button Control Loaded!'

try:
    if ac_detect:
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

finally:
    SetColor([0, 0, 0])
    #database.close()
