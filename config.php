<?php

/*
 * config.php - Parse Python config file to PHP variables
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


// Create variables from python config file
function parse_config($str) {
	if (preg_match("/^([\w\-]+)\s+\=\s+[0-9'\"]/", $str, $matches)) $var_name = $matches[1];
	if (preg_match("/\=\s+([\w\-.]+|'(.*?)')\s+/", $str, $matches)) $var_value = preg_replace('/^([\'"])(.*)\\1$/', '\\2', $matches[1]);
	
	if (!isset($var_name, $var_value)) return false;
	return array($var_name, $var_value);
}

// Python config file location
$config_file = dirname(__FILE__) . '/python/config.py';

// Verify file exists / permissions
if (!file_exists($config_file) || !is_readable($config_file)) {
	die($config_file . ' ' . $lang_config_not_readable);
}

// Read config file to array
$py_config = file($config_file, FILE_SKIP_EMPTY_LINES);

// Parse each line from array
foreach ($py_config as $line) {
	$parsed = parse_config($line);
	
	// Set variable if found
    if($parsed !== false) ${$parsed[0]} = $parsed[1];
}

?>
