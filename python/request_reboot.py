#!/usr/bin/python

# request_reboot.py - Return result before rebooting
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
import sys, json, subprocess

loc = None

try:
    loc = json.loads(sys.argv[1])
    
    # Now reboot as a subprocess
    reboot_script = subprocess.Popen(['python', loc + '/python/reboot.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    # Print JSON result
    print json.dumps({'result' : True})

except (ValueError, TypeError, IndexError, KeyError) as e:
    print json.dumps({'error': str(e)})