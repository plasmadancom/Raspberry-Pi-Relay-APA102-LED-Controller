#!/usr/bin/python

# motor.py - Blind / shutter motor up / down control
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

motor_direction = 1 if swap_motor_direction else 0           # motor_direction = 1 should always be UP, even if swapped
motor_steps = int(motor_timer * 20)
motor_pos = 0
auto_limit = 0

if motor_auto_up_limit > 0:
    auto_limit = int(max(0, (motor_steps / 100) * motor_auto_up_limit))

def stop(swap=1):
    global motor_direction
    
    wiringpi.digitalWrite(motor_pwr, 0)                      # Stop motor_pwr
    wiringpi.digitalWrite(motor_relay, 0)                    # Stop motor_relay
    
    if swap:
        motor_direction = not motor_direction                # Swap motor motor_direction

def position(u):
    global motor_pos
    
    if u == 0:
        motor_pos = 0                                        # Reset
    
    else:
        motor_pos = max(min(motor_steps, motor_pos + u), 0)  # Clamp limits
    
    print motor_pos

def presshold(going_up=0):
    if going_up:
        position(int(motor_delay * 20))                      # Adjust for motor delay
    
    else:
        position(-int(motor_delay * 20))
    
    if not wiringpi.digitalRead(button2):                    # Still pressing! Don't use timer
        while not wiringpi.digitalRead(button2):             # Re-check...
            sleep(0.05)
            
            if going_up:
                position(1)
            
            else:
                position(-1)
    
    else:                                                    # Use timer
        range_steps = motor_steps if going_up else int(motor_steps + motor_down_extended * 20)
        
        for i in range(range_steps):
            sleep(0.05)
            
            if going_up:
                position(1)
            
            else:
                position(-1)
            
            if not wiringpi.digitalRead(button2) or wiringpi.digitalRead(buffer2) or wiringpi.digitalRead(buffer3) or wiringpi.digitalRead(buffer4) or (going_up and auto_limit and auto_limit == motor_pos):
                break                                        # Interrupt timer
            
            if i == range_steps:                             # Cycle complete
                if going_up:
                    position(i)                              # Upper limit
                
                else:
                    position(0)                              # Reset position

def start(relay=0, swap=1):
    if relay:
        wiringpi.digitalWrite(motor_relay, 1)                # Start motor_relay
        sleep(motor_direction_delay)                         # Wait for relay
    
    wiringpi.digitalWrite(motor_pwr, 1)                      # Start motor_pwr
    sleep(motor_delay)
    
    going_up = 1 if relay or (not relay and swap_motor_direction) else 0
    
    presshold(going_up)                                      # Use timer?
    stop(swap)                                               # Stop & swap motor motor_direction

buffer_up = buffer3 if swap_motor_direction else buffer2     # Swap buffer2 & buffer3 if swap_motor_direction is set
buffer_down = buffer2 if swap_motor_direction else buffer3

print 'Motor Button Control Loaded!'

try:
    while True:                                              # Loop forever
        if not wiringpi.digitalRead(button2) or wiringpi.digitalRead(buffer4):
            if wiringpi.digitalRead(motor_pwr):              # Already running? (Maybe the web GUI triggered it)
                stop()
            
            elif motor_direction:
                start(1)                                     # Up
            
            else:
                start()                                      # Down
            
            sleep(button2_delay)                             # Delay
        
        elif wiringpi.digitalRead(buffer_up):                # If buffer_up (Motor UP) is triggered (by the web GUI)
            if wiringpi.digitalRead(motor_pwr):              # Already running? (Maybe button2 triggered it)
                stop()
            
            else:
                start(1)                                     # Up
            
            sleep(button2_delay)                             # Delay
        
        elif wiringpi.digitalRead(buffer_down):              # If buffer_down (Motor DOWN)is triggered (by the web GUI)
            if wiringpi.digitalRead(motor_pwr):              # Already running? (Maybe button2 triggered it)
                stop()
            
            else:
                start()                                      # Down
            
            sleep(button2_delay)                             # Delay

except Exception as e:                                       # Something went wrong
    print e