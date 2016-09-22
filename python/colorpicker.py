#!/usr/bin/python

# colorpicker.py - Parse data from web GUI
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
import sys, json
from config import *
from io import *
from functions import *

data = None
result = False
text = lang_success

try:
    data = json.loads(sys.argv[1])
    
    # Change color
    def colorpickerColor(data):
        if transition_effect == 'wipe':
            SetColor(data, 1, data[-1], 0)
        
        elif transition_effect == 'fade':
            ColorFade(data, data[-1], 0)
        
        else:
            SetColor(data, 0, data[-1], 0)
        
        return True
    
    # Change brigtness
    def colorpickerBrightness(data):
        fadeBrightness(data[0], 0)
        
        return True
    
    if ac_detect and not wiringpi.digitalRead(ac_detect_port_1):
        text = lang_ac_detect_error
    
    elif len(data) == 1:
        result = colorpickerBrightness(data)
    
    elif len(data) == 4:
        result = colorpickerColor(data)
    
    # Print JSON result
    print json.dumps({'result' : result, 'text' : text, 'received' : data})

except (ValueError, TypeError, IndexError, KeyError) as e:
    text = json.dumps({'error': str(e)})
    print text