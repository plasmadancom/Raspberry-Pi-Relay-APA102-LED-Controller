<?php

/*
 * submit.php - Get POST data from web GUI
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
require_once 'functions.php';

$result = array();

### DATA REQUESTS

// System status
if (isset($_POST['system_status'])) {
	// If we can return a value Apache must be running
	$result['system_status'] = 1;
}

// Get color from file
if (isset($_POST['request_color'])) {
	$result['color'] = GetColor();
}

// Get GPIO status of port
if (isset($_POST['gpio_pins']) && is_array($_POST['gpio_pins'])) {
	// Loop each request
	foreach($_POST['gpio_pins'] as $pin) {
		if (!is_numeric($pin)) continue;
		
		$result['gpio_status'][$pin] = gpio_status($pin);
	}
}

### ACTIONS

// Relay channel 1
else if (isset($_POST['relay_ch1'])) {
	$result[] = relay_toggle($relay_1);
}

// Relay channel 2
else if (isset($_POST['relay_ch2'])) {
	$result[] = relay_toggle($relay_2);
}

// Preset
else if (isset($_POST['preset'])) {
	$result[] = write_buffer($buffer1);
}

// Motor UP
else if (isset($_POST['motor_1'])) {
	$result[] = write_buffer($buffer2);
}

// Motor DOWN
else if (isset($_POST['motor_2'])) {
	$result[] = write_buffer($buffer3);
}

// Reset Pi
else if (isset($_POST['system_reset'])) {
	$result[] = shell_exec('sudo python ' . dirname(__FILE__) . '/python/request_reboot.py ' . escapeshellarg(json_encode(dirname(__FILE__))));
}

// RGB color
else if (! isset($_POST['color'])) {
	$result['error'] = $lang_submit_data_missing;
}

### COLORPICKER

// Confirm color data is array
else if (! is_array($_POST['color'])) {
	$result['error'] = $lang_submit_data_invalid;
}

// Confirm required values are present
else if (! ((isset($_POST['color'][0]) && count($_POST['color'] == 1)) || (
			isset($_POST['color'][0]) && 
			isset($_POST['color'][1]) && 
			isset($_POST['color'][2]) && 
			isset($_POST['color'][3])
		))) {
	$result['error'] = $lang_submit_array_data_missing;
}

// Confirm no erroneous data present
else if (! (count($_POST['color'] == 1) || count($_POST['color'] == 4))) {
	$result['error'] = $lang_submit_erroneous_data;
}

// Validate
else if (! ((count($_POST['color']) == 1 && is_numeric($_POST['color'][0])) || (
			count($_POST['color']) == 4 && 
			is_numeric($_POST['color'][0]) && 
			is_numeric($_POST['color'][1]) && 
			is_numeric($_POST['color'][2]) && 
			is_numeric($_POST['color'][3])
		))) {
	$result['error'] = $lang_submit_array_data_invalid;
}

// Sanity check
else if (! ((count($_POST['color']) == 1 && $lux_lowest <= $_POST['color'][0] && $_POST['color'][0] <= $lux_highest) || (
			count($_POST['color']) == 4 && 
			0 <= $_POST['color'][0] && $_POST['color'][0] <= 255 && 
			0 <= $_POST['color'][1] && $_POST['color'][1] <= 255 && 
			0 <= $_POST['color'][2] && $_POST['color'][2] <= 255 && 
			$lux_lowest <= $_POST['color'][3] && $_POST['color'][3] <= $lux_highest
		))) {
	$result['error'] = $lang_submit_failed_sanity_checks;
}

else {
	// Convert to integers
	foreach($_POST['color'] as $key => $value) {
		$_POST['color'][$key] = (int)$value;
	}
	
	// Sebmit color data
	$result[] = shell_exec('sudo python ' . dirname(__FILE__) . '/python/colorpicker.py ' . escapeshellarg(json_encode($_POST['color'])));
}

echo json_encode($result);

?>
