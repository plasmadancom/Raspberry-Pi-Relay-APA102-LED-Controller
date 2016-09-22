#!/usr/bin/python

# strip.py - Declare & initialize strip using dotstar.c library
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
from dotstar import Adafruit_DotStar                         # Must be in same directory. Source: https://learn.adafruit.com/adafruit-dotstar-leds

strip = Adafruit_DotStar(numpixels, spi, order=rgb_order)    # Declare strip. See https://learn.adafruit.com/adafruit-dotstar-leds

strip.begin()                                                # Initialize pins for output