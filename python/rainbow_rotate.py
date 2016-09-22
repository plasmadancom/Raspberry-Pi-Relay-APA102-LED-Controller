#!/usr/bin/python

# rainbow_rotate.py - Rotating rainbow effect (EXPERIMENTAL)
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
from strip import *
from functions import *

steps = 255                                                  # Steps per cycle
scale = 255.0 / numpixels                                    # Index change between each LED
shift = scale * rainbow_start                                # Adjust start position from config

currentCycle = 0

lux = validateBrightness(GetColor()[-1])

strip.begin()                                                # Initialize pins for output
strip.setBrightness(lux)                                     # Set lux level

while True:
    for step in range (steps):
        start = 255 / steps * (step + shift)                 # Value of LED 0
        
        for i in range(numpixels):
            ledIndex = start + i * scale                     # Index of LED i, not rounded / wrapped at 255
            wrapped = int(round(ledIndex, 0)) % 255          # Rounded and wrapped
            
            color = ColorWheel(wrapped)                      # Get the combined color out of the wheel
            
            strip.setPixelColor(i,color)
            #CachePixel(i, color, lux)
        
        strip.show()
    
    currentCycle += 1