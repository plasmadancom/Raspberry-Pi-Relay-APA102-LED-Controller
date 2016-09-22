<?php

/*
 * functions.php - Functions needed for web GUI
 * 
 * Copyright (C) 2016 Dan Jones - https://plasmadan.com
 * 
 * Full project details here:
 * https://github.com/plasmadancom/Raspberry-Pi-Relay-APA102-LED-Controller
 * https://www.avforums.com/threads/ongoing-plasmadans-living-room-cinema-office-build.1992617/
 * 
 * -----------------------------------------------------------------------------
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * -----------------------------------------------------------------------------
 */


require_once 'config.php';

// Validate color
function validate_col($val) {
	global $lux_lowest, $lux_highest;
	
	return ($val >= $lux_lowest && $val <= $lux_highest);
}

// Read color from file
function read_color_file($file) {
	// Get file cotents as array
	$color = @file($file);
	
	return $color;
}

// Create color file
function write_color_file($file, $fallback) {
	// Create file
	$file = fopen($file, "a");
	
	// Write to file and close
	fwrite($file, implode(PHP_EOL, $fallback));
	fclose($file);
}

// Convert 24-bit color to RGB
function colorToRGB($c) {
    $c = (int)$c;
    
    $r = $c >> 16;
    $c -= $r * 65536;
    $g = $c / 256;
    $c -= $g * 256;
    $b = $c;
    
    return array((string)$r, (string)$g, (string)$b);
}

// Get color from file
function GetColor() {
	global $numpixels;
	
	// File location
	$color_file = dirname(__FILE__) . '/color.txt';
	
	// fallback color
	$fallback = array('r' => 255, 'g' => 255, 'b' => 255, 'l' => 128);
	
	// Check for existing color file
	if(!file_exists($color_file)) write_color_file($color_file, $fallback);
	
	// Check if color file is readable
	if(!is_readable($color_file)) die($color_file . ' is not readable! Check the file permissions.');
	
	// Get color from file
	$color = read_color_file($color_file);
	
	// Verify color file data
	if (empty($color)) {
		write_color_file($color_file, $fallback);
		return $fallback;
	}
	
	// Single 24-bit color & brightness, convert to RGB
	else if (count($color) == 2) {
		$rgb = colorToRGB($color[0]);
		$color = array_map('intval', array($rgb[0], $rgb[1], $rgb[2], end($color)));
	}
	
	// Multiple 24-bit colors & brightness. Can't display this in the GUI (yet), just get the first color
	else if (count($color) == $numpixels + 1 || count($color) == $numpixels + 2) {
		$rgb = colorToRGB($color[0]);
		$color = array_map('intval', array($rgb[0], $rgb[1], $rgb[2], end($color)));
	}
	
	return array_map('intval', $color);
}

// Return GPIO status
function gpio_status($pin) {
	exec("gpio read " . $pin, $status);
	return $status[0];
}

// Toggle GPIO state & return
function relay_toggle($pin) {
	$status = (bool)gpio_status($pin) ? 0 : 1;
	
	system("gpio mode " . $pin . " out");
	system("gpio write " . $pin . " " . $status);
	
	return gpio_status($pin);
}

// Write to spare GPIO port for Python to detect
function write_buffer($pin) {
	global $buffer_sleep;
	
	// Write high to GPIO, wait, reset
	system("gpio write $pin 1");
	usleep($buffer_sleep);
	system("gpio write $pin 0");
	
	return 1;
}

?>