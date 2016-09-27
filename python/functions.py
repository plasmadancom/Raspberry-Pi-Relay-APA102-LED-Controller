#!/usr/bin/python

# functions.py
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
#import cPickle, sqlite3

from time import sleep
from bisect import bisect_left
from config import *
from io import *
from strip import *

# SQLite in-memorty database connection (EXPERIMENTAL)
# Seems SQLite in-memory database connections by URI require Python 3 to work!
if save_caching:
    database = sqlite3.connect("file:colcache1?mode=memory&cache=shared")

pixel_cache = []
rainbow_last_step = 0

# Poll preset button press
def PollPreset():
    return (not wiringpi.digitalRead(button1) or wiringpi.digitalRead(buffer1))

# Return one 24-bit color value 
def rgbToColor(r, g, b):
    return (int(r) << 16) + (int(g) << 8) + int(b)

# Convert 24-bit color value to RGB
def colorToRGB(c):
    c = int(c)
    
    r = c >> 16
    c -= r * 65536
    g = c / 256
    c -= g * 256
    b = c
    
    return [r, g, b]

# Notifier if invalid color format passed
def printValidFormats(complex=0):
    if complex:
        print ("{0}: [R, G, B], [R, G, B, {1}], [24-bit], [24-bit, {1}], [24-bit, 24-bit, ... (* numpixels), {1}]".format(lang_valid_colors, lang_setting_brightness))
        
    else:
        print ("{0}: [R, G, B], [R, G, B, {1}], [24-bit], [24-bit, {1}]".format(lang_valid_colors, lang_setting_brightness))

# Validate brightness & return
def validateBrightness(lux, save_off=0):
    if lux > lux_highest:
        return lux_highest                                   # Limit max
    
    elif lux < lux_lowest and not save_off:
        return lux_lowest                                    # Limit min
    
    return lux

# Get color from file / database
def GetColor(rgb=0):
    c = backup_col
    
    try:
        if not save_caching:
            raise ValueError()                               # Cancel
        
        cursor = database.cursor()
        
        query_db = "SELECT color FROM cache LIMIT 1"
        cursor.execute(query_db)                             # Query database
        
        res = cursor.fetchone()
        c = cPickle.loads(str(res[0]))                       # Unpickle
    
    except:
        if savefile and save_to_file:
            try:
                with open(savefile, 'r') as f:               # Get color & brightness from file
                    c = f.read().splitlines()
                
                if not c:
                    raise ValueError("File is blank: " + savefile)
            
            except (Exception, ValueError) as e:             # Something went wrong
                print e
                pass                                         # Nevermind, use backup instead
            
            pass
    
    if len(c) == 4:                                          # Single RGB color & brightness, convert to 24-bit
        if rgb:
            return map(int, [c[0], c[1], c[2], c[-1]])
        
        return map(int, [rgbToColor(c[0], c[1], c[2]), c[-1]])
    
    elif len(c) == 2 or len(c) == numpixels + 1:             # Single or multiple 24-bit colors & brightness
        if rgb:
            pos = shift_pixels % numpixels                   # Get the first color from starting position
            
            rgbl = colorToRGB(c[pos])
            rgbl.append(c[-1])
            
            return map(int, rgbl)
        
        return map(int, c)
    
    elif len(c) == numpixels + 2:                            # Multiple 24-bit colors & brightness with effect
        lux = [int(c[-1])]                                   # Brightness
        effect = [c[-2]]                                     # Effect name
        
        if rgb:
            pos = shift_pixels % numpixels                   # Get the first color from starting position
            
            rgbl = colorToRGB(c[pos])
            rgbl.append(c[-1])
            
            return map(int, rgbl) + effect + lux
        
        c.pop()                                              # Drop brightness from end of list
        c.pop()                                              # Drop effect name from end of list
        
        return map(int, c) + effect + lux                    # Return colors, effect name & brightness
    
    else:
        print ("{0}: {1}, {2}".format(lang_invalid_file, len(c), savefile))
    
    if rgb:
        return [backup_col[0], backup_col[1], backup_col[2], backup_col[-1]]
    
    return [rgbToColor(backup_col[0], backup_col[1], backup_col[2]), backup_col[-1]]

# Save color & brightness to file / database
def SaveCol(c, save_off=0, lux=0):
    if not isinstance(c, list):                              # Incorrect data passed
        printValidFormats(1)
        return
    
    if not save_off and c[0] == 0 and c[1] == 0 and c[2] == 0:
        return                                               # Don't save off state, use existing colors
    
    if len(c) == 1 or len(c) == 3 or len(c) == numpixels:
        lux = lux if lux else GetColor()[-1]                 # Use old color if brightness not set
    
    elif len(c) == 2 or len(c) == 4 or len(c) == numpixels + 1 or len(c) == numpixels + 2:
        lux = lux if lux else c[-1]                          # Use passed color if brightness not set
    
    lux = validateBrightness(lux, save_off)                  # Validate brightness level
    
    s = c[:]                                                 # I hate you Python
    
    if len(c) == 1 or len(c) == 2:
        s = colorToRGB(c[0])                                 # Convert to RGB for easier readability
        s.append(lux)
    
    elif len(c) == 3 or len(c) == numpixels:                 # No brigtness passed, add it
        s.append(lux)
    
    else:
        s.pop()                                              # Override passed brightness
        s.append(lux)
    
    if save_caching:
        db_table = "CREATE TABLE IF NOT EXISTS cache(id INTEGER PRIMARY KEY, color BLOB)"
        database.execute(db_table)                           # Create database table on first run
        
        pdata = cPickle.dumps(s)                             # Pickle
        
        db_update = "INSERT OR REPLACE INTO cache (id, color) VALUES (1, ?)"
        database.execute(db_update, [buffer(pdata)])         # Update / insert pickle into database
        
        database.commit()
    
    if savefile and save_to_file:
        try:
            with open(savefile, 'wb') as f:                  # Save new colors & brightness to text file for next boot
                for line in s:
                    print >> f, line
        
        except Exception as e:                               # Something went wrong
            print e
            pass                                             # Pass anyway, since we can always use the backup

# Save single pixel color
def CachePixel(pixel, color):
    global pixel_cache
    
    if not pixel_cache:                                      # Populate pixel_cache if empty
        pixel_cache = [1] * numpixels
    
    pixel_cache[pixel] = color

# Cache all pixels
def CachePixels(col=0):
    global pixel_cache
    
    c = col if col else GetColor()                           # Get color in 24-bit mode
    
    if len(c) == numpixels + 1 or len(c) == numpixels + 2:   # Multiple 24-bit colors
        for i in range(numpixels):
            CachePixel(i, c[i])                              # Cache each pixel color
    
    else:
        for i in range(numpixels):
            CachePixel(i, c[0])                              # Cache each pixel color
    
    return pixel_cache

# Set all LEDs from single 24-bit color
def SolidColor(c, lux, wipe=0, cache=1):
    strip.setBrightness(lux)                                 # Set brightness level
    
    for i in range(numpixels):
        start = (i + shift_pixels) % numpixels               # Shift LED start position by shift_pixels
        
        strip.setPixelColor(start, c)                        # Set each pixel color
        
        if cache:
            CachePixel(start, c)
            
        if wipe:
            strip.show()                                     # Light up this pixel
    
    if not wipe:
        strip.show()                                         # Light up the strip

# Set all LEDs one color
def SetColor(c, wipe=0, lux=0, cache=1, save_off=0):
    if not isinstance(c, list):                              # Incorrect data passed
        printValidFormats(1)
        return
    
    if len(c) == 1 or len(c) == 3 or len(c) == numpixels:
        lux = lux if lux else GetColor()[-1]                 # Use old color if brightness not set
    
    elif len(c) == 2 or len(c) == 4 or len(c) == numpixels + 1:
        lux = lux if lux else c[-1]                          # Use passed color if brightness not set
    
    lux = validateBrightness(lux, save_off)                  # Validate brightness level
    
    if len(c) == 3 or len(c) == 4:                           # Single RGB color (& brightness?)
        color = rgbToColor(c[0], c[1], c[2])                 # Convert color to 24-bit
        
        SolidColor(color, lux, wipe, cache)                  # Run
    
    elif len(c) == 1 or len(c) == 2:                         # 24-bit color & (& brightness?)
        SolidColor(c[0], lux, wipe, cache)                   # Run
    
    elif len(c) == numpixels or len(c) == numpixels + 1:     # Multiple 24-bit colors (& brightness?)
        for i in range(numpixels):
            strip.setPixelColor(i, c[i])                     # Set each pixel color
            
            if cache:
                CachePixel(i, c[i])
            
            if wipe:
                strip.show()                                 # Light up this pixel
        
        if not wipe:
            strip.show()                                     # Light up the strip
    
    else:
        print ("{0}: {1}".format(lang_invalid_color_data, c))
        return
    
    SaveCol(c, save_off, lux)

# Set all LEDs to colors from list
def SetPixels(c, lux=0, cache=1):
    if not isinstance(c, list):                              # Incorrect data passed
        printValidFormats(1)
        return
    
    lux = lux if lux else GetColor()[-1]
    strip.setBrightness(lux)                                 # Set brightness level
    
    for i in range(numpixels):                               # Set each pixel color
        strip.setPixelColor(i, c[i])
        
        if cache:
            CachePixel(i, c[i])
    
    strip.show()                                             # Light up the strip

# Return list of color transition steps between 0 - 255
def calculateColorFade(new, old, lux=0, save_off=0):
    new = int(new)
    old = int(old)
    
    step_val = (new - old) / color_fade_steps;               # Divide color transition into step values
    
    colors = []
    
    for i in range(0, color_fade_steps):
        color = int(round(new - (step_val * i)))             # Round each value to whole
        
        if lux:
            color = validateBrightness(color, save_off)      # Limit max brightness
        
        else:
            if color > 255:
                color = 255                                  # Limit max color
            
            elif color < 0:
                color = 0                                    # Limit min color
        
        colors.append(color)                                 # Add color to list
    
    return colors

# Color fade effect
def ColorFade(c, lux=0, cache=1, save_off=0):
    if not isinstance(c, list):                              # Incorrect data passed
        printValidFormats()
        return
    
    col = GetColor(1)                                        # Get color in RGB mode to use in calculation
    lux_fade = 0
    
    if len(c) == 2 or len(c) == 4 or lux:                    # Transition the brightness
        lux_fade = 1
    
    if len(c) == 1 or len(c) == 3:
        lux = lux if lux else col[-1]                        # Use old color if brightness not set
    
    elif len(c) == 2 or len(c) == 4:
        lux = lux if lux else c[-1]                          # Use passed color if brightness not set
    
    lux = validateBrightness(lux, save_off)                  # Validate brightness level
    
    if not len(c) == 3 and not len(c) == 4:                  # Not a single RGB color
        c = colorToRGB(c[0])                                 # Convert to RGB to use in calculation
    
    if lux_fade and not lux == col[-1]:
        lux_fade = calculateColorFade(lux, col[-1], 1, save_off)
    
    else:
        strip.setBrightness(lux)                             # Set brightness level
    
    rn = calculateColorFade(c[0], col[0])                    # Get red color transitions
    gn = calculateColorFade(c[1], col[1])                    # Get green color transitions
    bn = calculateColorFade(c[2], col[2])                    # Get blue color transitions
    
    for key, val in reversed(list(enumerate(rn))):
        color = rgbToColor(val, gn[key], bn[key])            # Convert color to 24-bit
        
        if lux_fade and not lux == col[-1]:
            strip.setBrightness(lux_fade[key])               # Set brightness level
        
        for i in range(numpixels):                           # Set each pixel color
            strip.setPixelColor(i, color)
            
            if cache:
                CachePixel(i, color)
        
        strip.show()                                         # Light up the strip
        sleep(color_fade_delay)
    
    SaveCol(c, save_off, lux)

# Brightness fade transition
def fadeBrightness(lux, cache=1, save_off=0):
    if not isinstance(lux, int):                             # Incorrect data passed
        return
    
    col = GetColor()                                         # Get color in 24-bit mode
    
    lux = validateBrightness(lux, save_off)                  # Validate brightness level
    
    if lux == col[-1]:                                       # They're the same, no point continuing
        return
    
    pixel_cache = CachePixels(col)                           # Update the pixel cache
    
    lux_fade = calculateColorFade(lux, col[-1], 1, save_off) # Get brightness fade transitions
    
    for i in reversed(lux_fade):
        SetPixels(pixel_cache, i, cache)                     # Set colour / brightness of each pixel
        
        sleep(color_fade_delay)
    
    SaveCol(col, save_off, lux)

# Return color from wheel position
def ColorWheel(pos):
    if pos > 254: pos = 254                                  # Limit
    
    if pos < 85:                                             # Green - Red
        return rgbToColor(pos * 3, 255 - pos * 3, 0)
    
    elif pos < 170:                                          # Red - Blue
        pos -= 85
        return rgbToColor(255 - pos * 3, 0, pos * 3)
    
    else:                                                    # Blue - Green
        pos -= 170
        return rgbToColor(0, pos * 3, 255 - pos * 3);

# Rainbow effect
def Rainbow(wipe=0, save_off=0):
    lux = validateBrightness(GetColor()[-1])                 # Get color from file / database
    
    scale = 255.0 / numpixels                                # Index change between each LED
    rainbow_index = scale * rainbow_start                    # Starting position of rainbow effect (allows more control over colors)
    
    strip.setBrightness(lux)                                 # Set brightness level
    
    colors = [None] * numpixels                              # Create list of indexes
    
    for i in range(numpixels):
        ledIndex = rainbow_index + i * scale                 # Index of LED i, not rounded / wrapped at 255
        wrapped = int(round(ledIndex, 0)) % 255              # Rounded and wrapped
        
        color = ColorWheel(wrapped)                          # Get the combined color out of the wheel
        
        start = (i + shift_pixels) % numpixels               # Shift LED start position by shift_pixels
        
        colors[start] = color
        strip.setPixelColor(start, color)
        
        CachePixel(start, color)
        
        if wipe:
            strip.show()
    
    if not wipe:
        strip.show()
    
    colors.append('rainbow')                                 # Store the effect name at index -2
    colors.append(lux)
    
    SaveCol(colors, save_off)

# Rainbow rotate effect
def RainbowRotate(cont=0, save_off=0):
    global rainbow_last_step
    
    if not cont:
        rainbow_last_step = 0                                # Reset to start
    
    lux = validateBrightness(GetColor()[-1])                 # Get color from file / database
    
    steps = 255                                              # Steps per cycle
    scale = 255.0 / numpixels                                # Index change between each LED
    rainbow_index = (scale * rainbow_start) + rainbow_last_step
    
    strip.setBrightness(lux)                                 # Set brightness level
    
    colors = [None] * numpixels                              # Create list of indexes
    
    def loop():
        global rainbow_last_step
        
        old_rainbow_last_step = rainbow_last_step
        currentCycle = 0
        
        while True:                                          # Loop forever
            if PollPreset():                                 # Poll GPIO
                return
            
            for step in range (steps):
                rainbow_last_step = (step + old_rainbow_last_step) % steps
                
                start_index = 255 / steps * (step + rainbow_index)
                
                for i in range(numpixels):
                    if PollPreset():                         # Poll GPIO again
                        return
                    
                    ledIndex = start_index + i * scale
                    wrapped = int(round(ledIndex, 0)) % 255  # Rounded and wrapped
                    
                    color = ColorWheel(wrapped)              # Get the combined color out of the wheel
                    
                    start = (i + shift_pixels) % numpixels   # Shift LED start position by shift_pixels
                    
                    colors[start] = color
                    strip.setPixelColor(start, color)
                    
                    CachePixel(start, color)
                
                strip.show()
            
            currentCycle += 1
    
    loop()
    
    colors.append('rainbowrotate')                           # Store the effect name at index -2
    colors.append(lux)
    
    SaveCol(colors, save_off)

# Return the closest index to num
def takeClosest(li, num):
    pos = bisect_left(li, num)                               # Find leftmost item greater than or equal to num
    if pos == 0:                                             # Start of list
        return li[0]
    
    if pos == len(li):                                       # End of list
        return li[-1]
    
    before = li[pos - 1]
    after = li[pos]
    
    if after - num < num - before:                           # Return the smallest num
        return after
    
    return before

# Find preset index position if exists
def SearchIndex():
    col = GetColor()                                         # Get color in 34-bit mode
    
    if isinstance(col[-2], basestring):                      # Preset name (string)
        try:
            return preset.index(col[-2])
        
        except:
            pass
    
    try:
        return preset.index([col[0]])                        # Matched 24-bit color
    
    except:
        pass
    
    try:
        return preset.index(colorToRGB(col[0]))              # Matched RGB color
    
    except:
        pass
    
    if preset_idx <= len(col):
        return preset_idx                                    # Use default
    
    return 0

# Get current & next preset index
def GetPresetIndex(jump=0):
    idx = SearchIndex()                                      # Default or manual starting preset index
    
    if jump:
        idx += jump
    
    next_idx = (idx + 1) % len(preset)                       # Shift preset index by 1
    
    return [idx, next_idx]

# Cycle through preset modes
def cyclePreset(pwr_cycle=0, jump=0):
    idxs = GetPresetIndex(jump)
    
    curr_mode = preset[idxs[0]]                              # Select preset index from list
    next_mode = preset[idxs[1]]                              # Select preset index from list
    
    if next_mode == 'rainbowrotate':                         # Rainbow rotate effect
        Rainbow(not pwr_cycle and wipe_effects)
        RainbowRotate()
    
    elif next_mode == 'rainbow':                             # Rainbow effect
        Rainbow(not pwr_cycle and wipe_effects)
    
    elif isinstance(next_mode, basestring):                  # Preset is an effect, but isn't implemented!
        print ("{0} '{1}' {2}".format(lang_preset, next_mode, lang_not_implemented))
        
        cyclePreset(pwr_cycle, idxs[1])                      # Start again at next index...
    
    elif pwr_cycle:
        SetColor(next_mode)
    
    elif isinstance(curr_mode, basestring) or len(GetColor()) > 4:
        SetColor(next_mode, wipe_effects)                    # Force wipe transition
    
    elif transition_effect == 'wipe':
        SetColor(next_mode, 1)                               # Wipe transition
    
    elif transition_effect == 'fade':
        ColorFade(next_mode)
    
    else:
        SetColor(next_mode)                                  # No transition
