#!/usr/bin/python

# motor.py - Blind control from single push-to-make
# 
# CAUTION!! This script is meant to be used with automatic blind / shutter / projector screen motors with mechanical limits.
# Do not use with the wrong type of motor or you may overwind your blind and damage something!
# You should use the 4-core cabled type with 2 x Lives (Up & Down)
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

def stop(swap=1):
    global motor_direction
    
    wiringpi.digitalWrite(motor_pwr, 0)                      # Stop motor_pwr
    wiringpi.digitalWrite(motor_relay, 0)                    # Stop motor_relay
    
    if swap:
        motor_direction = not motor_direction                # Swap motor motor_direction

def presshold():
    if not wiringpi.digitalRead(button2):                    # Still pressing! Don't use timer
        while not wiringpi.digitalRead(button2):             # Re-check...
            sleep(0.05)
    
    else:                                                    # Use timer
        for i in range(motor_timer*20):
            sleep(0.05)
            
            if not wiringpi.digitalRead(button2) or wiringpi.digitalRead(buffer2) or wiringpi.digitalRead(buffer3):
                break                                        # Interrupt timer

def start(relay=0, swap=1):
    if relay:
        wiringpi.digitalWrite(motor_relay, 1)                # Start motor_relay
        sleep(motor_direction_delay)                         # Wait for relay
    
    wiringpi.digitalWrite(motor_pwr, 1)                      # Start motor_pwr
    sleep(motor_delay)
    
    presshold()                                              # Use timer?
    stop(swap)                                               # Stop & swap motor motor_direction

print 'Motor Button Control Loaded!'

while True:                                                  # Loop forever
    if not wiringpi.digitalRead(button2):                    # If button2 is pressed
        if wiringpi.digitalRead(motor_pwr):                  # Already running? (Maybe the web GUI triggered it)
            stop()
        
        elif motor_direction:
            start(1)
        
        else:
            start()
        
        sleep(button2_delay)                                 # Delay
    
    elif wiringpi.digitalRead(buffer2):                      # If buffer2 is triggered (by the web GUI)
        if wiringpi.digitalRead(motor_pwr):                  # Already running? (Maybe button2 triggered it)
            stop()
        
        else:
            start(1)
        
        sleep(button2_delay)                                 # Delay
    
    elif wiringpi.digitalRead(buffer3):                      # If buffer3 is triggered (by the web GUI)
        if wiringpi.digitalRead(motor_pwr):                  # Already running? (Maybe button2 triggered it)
            stop()
        
        else:
            start()
        
        sleep(button2_delay)                                 # Delay
