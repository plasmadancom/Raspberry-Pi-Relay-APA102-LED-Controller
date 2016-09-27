/*
 * functions.js
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


// Config
var autoupdate = $('#autoupdate').val() > 0 ? true : false;
var ajax_timeout = $('#ajax_timeout').val() ? parseInt($('#ajax_timeout').val()) : 5000;
var refreshtimer = $('#refreshtimer').val() ? parseInt($('#refreshtimer').val()) : 1000;
var min_l = $('#minbrightness').val() && parseInt($('#minbrightness').val()) > 0 ? parseInt($('#minbrightness').val()) : 0;
var max_l = $('#maxbrightness').val() && parseInt($('#maxbrightness').val()) < 255 ? parseInt($('#maxbrightness').val()) : 255;
var ac_detect = $('#ac_detect').val() > 0 ? true : false;
var ac_detect_port_1 = parseInt($('#ac_detect_port_1').val());
var ac_detect_port_2 = parseInt($('#ac_detect_port_2').val());
var relay_1 = parseInt($('#relay_1').val());
var relay_2 = parseInt($('#relay_2').val());

// Settings
var red = $('#red').val() ? parseInt($('#red').val()) : 255;
var green = $('#green').val() ? parseInt($('#green').val()) : 255;
var blue = $('#blue').val() ? parseInt($('#blue').val()) : 255;
var lux = $('#lux').val() ? parseInt($('#lux').val()) : 128;

// Language / fail-over
var lang_success = $('#lang_success').length > 0 ? $('#lang_success').val() : 'Success!';
var lang_warning = $('#lang_warning').length > 0 ? $('#lang_warning').val() : 'Warning!';
var lang_error = $('#lang_error').length > 0 ? $('#lang_error').val() : 'Error!';
var lang_ajax_error = $('#lang_ajax_error').length > 0 ? $('#lang_ajax_error').val() : 'AJAX response was null or empty!';
var lang_ajax_invalid = $('#lang_ajax_invalid').length > 0 ? $('#lang_ajax_invalid').val() : 'AJAX response was invalid!';
var lang_ajax_missing = $('#lang_ajax_missing').length > 0 ? $('#lang_ajax_missing').val() : 'AJAX response is missing data!';
var lang_setting = $('#lang_setting').length > 0 ? $('#lang_setting').val() : 'Setting';
var lang_setting_color = $('#lang_setting_color').length > 0 ? $('#lang_setting_color').val() : 'Color';
var lang_setting_brightness = $('#lang_setting_brightness').length > 0 ? $('#lang_setting_brightness').val() : 'Brightness';
var lang_set_color_mismatch = $('#lang_set_color_mismatch').length > 0 ? $('#lang_set_color_mismatch').val() : 'Set color did not match requested color! Result';
var lang_set_brightness_mismatch = $('#lang_set_brightness_mismatch').length > 0 ? $('#lang_set_brightness_mismatch').val() : 'Set brightness did not match requested brightness! Result';
var lang_switching = $('#lang_switching').length > 0 ? $('#lang_switching').val() : 'Switching';
var lang_cycling = $('#lang_cycling').length > 0 ? $('#lang_cycling').val() : 'Cycling preset...';
var lang_motor_up = $('#lang_motor_up').length > 0 ? $('#lang_motor_up').val() : 'up...';
var lang_motor_down = $('#lang_motor_down').length > 0 ? $('#lang_motor_down').val() : 'down...';
var lang_motor_toggle = $('#lang_motor_toggle').length > 0 ? $('#lang_motor_toggle').val() : 'Toggle motor';
var lang_reboot = $('#lang_reboot').length > 0 ? $('#lang_reboot').val() : 'Reboot the controller?';
var lang_cancel = $('#lang_cancel').length > 0 ? $('#lang_cancel').val() : 'Cancel';
var lang_rebooting = $('#lang_rebooting').length > 0 ? $('#lang_rebooting').val() : 'Rebooting controller...';
var lang_rebooting_inprogress = $('#lang_rebooting_inprogress').length > 0 ? $('#lang_rebooting_inprogress').val() : 'Controller reboot in progress...';
var lang_rebooting_slow = $('#lang_rebooting_slow').length > 0 ? $('#lang_rebooting_slow').val() : 'Taking longer than expected...';
var lang_rebooting_error = $('#lang_rebooting_error').length > 0 ? $('#lang_rebooting_error').val() : 'Please check the controller!';
var lang_rebooting_done = $('#lang_rebooting_done').length > 0 ? $('#lang_rebooting_done').val() : 'Controller online!';
var reboot_label = $('#system_reset').length > 0 ? $('#system_reset').text() : 'Reboot';

// On first load
$(document).ready(function() {
	// Update color
	updateColorpicker(red, green, blue, lux);
	
	if (autoupdate) {
		// Automaticly update after interval
		setInterval(function() {
			liveUpdateGUI();
		}, refreshtimer);
	}
	
	$.notifyDefaults({
		type: 'info',
		newest_on_top: true,
		placement: {
			align: 'center',
			from: 'bottom'
		},
		animate: {
			enter: 'animated fadeInUp',
			exit: 'animated fadeOut'
		}
	});
});

// wheelColorPicker combines sliderup with touchend, which causes problems
// Comment-out the wheelColorPicker attached touchend event and use this instead
var dragging = false;

$('html').on('touchmove', function() {
	dragging = true;
});

$('html').on('touchstart', function() {
	dragging = false;
});

// Catch mouse events
var mousemove = false;
var mousedown = false;

$('html').on('mousemove', function() {
	// Refers to wheelColorPicker slider wrapper or wheel
	var control = $($('body').data('jQWCP.activeControl'));
	
	// Set / unset mousedown var
	mousemove = control.length == 0 ? false : true;
}).mouseup(function() {
	mousedown = false;
});

$('.toggle, #preset').mousedown(function() {
	mousedown = true;
});

// Update wheelColorPicker
function updateColorpicker(r, g, b, l=255) {
	// Constrain brightness between range limit
	var luxL = ((l - min_l) / (max_l - min_l));
	
	// Update using custom setRgbal wheelColorPicker function
	$('.colorpicker').wheelColorPicker('setRgbal', r / 255, g / 255, b / 255, 1, luxL);
	
	// Update global color vars to compare against
	red = r;
	green = g;
	blue = b;
	lux = l;
}

// Nofity / logging function
function submit_notify(txt, time=5000) {
	var stripped = $('<i>' + txt + '</i>').text();
	console.log(stripped);
	
	// Defaults
	return $.notify(txt, {
		allow_dismiss: false,
		showProgressbar: true,
		delay: time
	});
}

// Error notify function
function error_notify(out='') {
	console.log(lang_error + ' ' + out);
	
	$.notifyClose();
	$.notify('<strong>' + lang_error + '</strong> ' + out, {
		type: 'danger',
		animate: {
			enter: '',
			exit: 'animated fadeOut'
		}
	});
}

// Warning notify function
function warning_notify(out='') {
	console.log(lang_warning + ' ' + out);
	
	$.notify('<strong>' + lang_warning + '</strong> ' + out, {
		type: 'warning',
		animate: {
			enter: 'animated fadeInUp',
			exit: 'animated fadeOut'
		}
	});
}

// Prevent double requests
var requestRunning = false;

function preventDoubleRequests(e=false, reset=false) {
	// Reset
	if (reset) {
		requestRunning = false;
		return;
	}
	
	// Check / Set
	else if (requestRunning) {
		// If event passed, catch it
		if (e) e.preventDefault();
		
		console.log('Warning! Prevented double AJAX request!');
		return true;
	}
	
	requestRunning = true;
	return false;
}

// Round to 2 decimal places if necessary
function round_x(x, n=0) {
	var x = n == 0 ? Math.round(x) : +x.toFixed(n);
	
	return x;
}

// Validate integers /strings of integers
function isNumeric(n) {
	return !isNaN(parseFloat(n)) && isFinite(n);
}

var haltupdate = false;

// Update status via AJAX
function liveUpdateGUI() {
	// Skip if mouse event
	if (mousedown || mousemove || dragging || haltupdate) return;
	
	// Get current color as object
	var cCol = $('.colorpicker').wheelColorPicker('getColor');
	
	// RGB
	var cR = round_x(cCol['r'] * 255);
	var cG = round_x(cCol['g'] * 255);
	var cB = round_x(cCol['b'] * 255);
	
	// Brightnes
	var cL = cCol['l'];
	
	// Convert position to contrained range
	var cluxL = (((max_l - min_l) * cL) + min_l) / 255;
	
	// Rounded & converted to 0-255 range
	var cluxR = round_x(cluxL * 255);
	
	// Update global color vars now so we don't need to wait for AJAX
	red = cR;
	green = cG;
	blue = cB;
	lux = cluxR;
	
	$.ajax({
		type: 'POST',
		data: {'request_color': 1, 'gpio_pins': [ac_detect_port_1, ac_detect_port_2, relay_1, relay_2]},
		dataType: 'json',
		url: '/submit.php',
		timeout: ajax_timeout,
		success: function(r) {
			if (!$.trim(r)) {
				error_notify(lang_ajax_error);
				return;
			}
			
			// Cancel update
			if (mousedown || mousemove || dragging || haltupdate) return;
			
			console.log('...');
			
			// Error
			if (typeof r['error'] !== 'undefined') {
				error_notify(r['error']);
				return;
			}
			
			// Missing result data
			else if (typeof r['gpio_status'] === 'undefined' || typeof r['color'] === 'undefined') {
				error_notify(lang_ajax_missing);
				return;
			}
			
			var rp = r['gpio_status'];
			var rc = r['color'];
			
			if (Object.keys(rp).length !== 4 || Object.keys(rc).length !== 4) {
				error_notify(lang_ajax_error);
				return;
			}
			
			// Check for ac_detect
			var ch1_gpio = ac_detect ? ac_detect_port_1 : relay_1;
			var ch2_gpio = ac_detect ? ac_detect_port_2 : relay_2;
			
			// Toggle checkboxes
			var ch1 = rp[ch1_gpio] == 1 ? true : false;
			var ch2 = rp[ch2_gpio] == 1 ? true : false;
			
			if (ch1 !== $('#relay_ch1').is(':checked')) {
				$('#relay_ch1').prop('checked', ch1).change();
				$('#relay_ch1').bootstrapToggle('destroy');
				$('#relay_ch1').bootstrapToggle();
			}
			
			if (ch2 !== $('#relay_ch2').is(':checked')) {
				$('#relay_ch2').prop('checked', ch2).change();
				$('#relay_ch2').bootstrapToggle('destroy');
				$('#relay_ch2').bootstrapToggle();
			}
			
			// Validate
			if (! (isNumeric(rc[0]) && isNumeric(rc[1]) && isNumeric(rc[2]) && isNumeric(rc[3]))) {
				error_notify(lang_ajax_invalid);
				return;
			}
			
			// Check if unchanged
			if ((rc[0] == cR && rc[1] == cG && rc[2] == cB && rc[3] == cluxR)) {
				// Nothing to do
				return;
			}
			
			// Update color
			updateColorpicker(rc[0], rc[1], rc[2], rc[3]);
		},
		error: function(xhr, textStatus, errorThrown) {
			try {
				error_notify(JSON.parse(xhr.responseText));
			}
			catch(e) {
				error_notify(textStatus);
			}
		}
	});
}

// Timer
var haltupdatetimer = false;

// Halt liveUpdateGUI() until complete
function haltLiveUpdate(clear=false) {
	if (clear) {
		try {
			clearTimeout(haltupdatetimer);
		}
		catch(er) {}
		
		haltupdate = false;
		
		return;
	}
	
	try {
		clearTimeout(haltupdatetimer);
	}
	catch(er) {}
	
	// Clear after refreshtimer * 2
	haltupdatetimer = setTimeout(function() {
		haltupdate = false;
	}, refreshtimer*2);
}

// On wheelColorPicker change
function colorPickerChanged(e, elm) {
	// Get color as object
	var color = elm.wheelColorPicker('getColor');
	
	// Force clear wheelColorPicker active control reference
	$('body').data('jQWCP.activeControl', null);
	
	// Prevent double requests
	if (preventDoubleRequests(e)) {
		warning_notify('Too fast!');
		
		return;
	}
	
	// Force hold
	haltLiveUpdate(true);
	haltupdate = true;
	
	// RGB
	var r = color['r'];
	var g = color['g'];
	var b = color['b'];
	
	// Brightness
	var l = color['l'];
	
	// Convert position to contrained range
	var luxL = (((max_l - min_l) * l) + min_l) / 255;
	
	// Rounded & converted to 0-255 range
	var rR = round_x(r * 255);
	var gR = round_x(g * 255);
	var bR = round_x(b * 255);
	var lR = round_x(luxL * 255);
	
	// Percentage of rounded value
	var lR_percent = round_x((100 / 255) * lR, 2);
	
	if (rR == red && gR == green && bR == blue) {
		// Only changed brightness
		var json = [lR];
		var notify_text = lang_setting + ' ' + lang_setting_brightness.toLowerCase() + ': ' + lR + ' (' + lR_percent + '%)';
	}
	
	else {
		var json = [rR, gR, bR, lR];
		var notify_text = lang_setting + ' ' + lang_setting_color.toLowerCase() + ': rgb(' + rR + ', ' + gR + ', ' + bR + ') / ' + lang_setting_brightness + ': ' + lR + ' (' + lR_percent + '%)';
	}
	
	// Update global color vars now so we don't need to wait for AJAX
	red = rR;
	green = gR;
	blue = bR;
	lux = lR;
	
	// Log to console so we know what's being sent
	var notify = submit_notify(notify_text);
	
	// Submit to controller via AJAX...
	$.ajax({
		type: 'POST',
		data: {'color': json},
		dataType: 'json',
		url: '/submit.php',
		timeout: ajax_timeout,
		success: function(r) {
			if (!$.trim(r)) {
				error_notify(lang_ajax_error);
				return;
			}
			/*
			// Error
			if (typeof r['error'] !== 'undefined') {
				error_notify(r['error']);
				return;
			}
			*/
			var rP = JSON.parse(r[0]);
			
			// Error
			if (typeof rP['error'] !== 'undefined') {
				error_notify(rP['error']);
				return;
			}
			
			// Missing result data
			if (typeof rP['result'] === 'undefined' || typeof rP['received'] === 'undefined' || typeof rP['text'] === 'undefined') {
				error_notify(lang_ajax_missing);
				return;
			}
			
			var result = rP['result'];
			var out = rP['text'];
			var c = rP['received'];
			
			// Confirm result
			if (!result) {
				$('#relay_ch1').bootstrapToggle('destroy');
				$('#relay_ch1').bootstrapToggle({
					offstyle: 'danger'
				});
				
				error_notify(out);
			}
			
			// Validate color
			else if (json == [rR, gR, bR, lR]) {
				if (! (parseInt(c[0]) == rR && parseInt(c[1]) == gR && parseInt(c[2]) == bR && parseInt(c[3]) == lR)) {
					var out = lang_set_color_mismatch + ': rgb(' + c[0] + ', ' + c[1] + ', ' + c[2] + '), ' + lang_setting_brightness + ': ' + c[3] + ' (' + round_x((100 / 255) * c[3], 2) + '%)';
					
					error_notify(out);
				}
				
				// Update global color vars to compare against
				red = parseInt(c[0]);
				green = parseInt(c[1]);
				blue = parseInt(c[2]);
				lux = parseInt(c[3]);
			}
			
			// Validate brightness
			else if (json == [lR]) {
				if (parseInt(c[3]) !== lR) {
					var out = lang_set_brightness_mismatch + ': ' + c[3] + ' (' + round_x((100 / 255) * c[3], 2) + '%)';
					
					error_notify(out);
				}
				
				// Update global brightness var to compare against
				lux = parseInt(c[3]);
			}
			
			notify.update({'type': 'success', 'message': '<strong>' + out + '</strong>', 'progress': 100});
		},
		complete: function() {
			preventDoubleRequests(0, true);
			
			// Wait for Python before allowing LiveUpdateGUI to run
			haltLiveUpdate();
		},
		error: function(xhr, textStatus, errorThrown) {
			preventDoubleRequests(0, true);
			
			// Clear on AJAX error, but wait for Python anyway
			haltLiveUpdate();
			
			try {
				error_notify(JSON.parse(xhr.responseText));
			}
			catch(e) {
				error_notify(textStatus);
			}
		}
	});
}

// Only if NOT touchmove
$('.colorpicker').on('sliderup', function(e) {
	if (dragging) {
		return;
	}
	
	colorPickerChanged(e, $(this));
});

// Only if touchmove
$('html').on('touchend', function(e) {
	if (!dragging) {
		return;
	}
	
	// Refers to wheelColorPicker slider wrapper or wheel
	var control = $($('body').data('jQWCP.activeControl'));
	
	if (control.length !== 0) {
		colorPickerChanged(e, $('.colorpicker'));
	}
});

// Relays
$('label[class="toggle"]').on('click', function() {
	var elm = $(this).find('.relay_checkbox');
	
	// Prevent double requests
	if (preventDoubleRequests()) {
		return;
	}
	
	// Force hold
	haltupdate = true;
	
	var ch = elm.data('relay');
	var state = elm.is(':checked') ? 1 : 0;
	
	// State is reversed because this is a click event, not a change event
	var state_name = state ? 'off' : 'on';
	var label = elm.parent().parent().parent().parent().find('.switch_label').text();
	
	var notify = submit_notify('<strong>' + lang_switching + ' ' + state_name + ' ' + label + '...</strong>');
	
	$.ajax({
		type: 'POST',
		url: '/submit.php',
		data: 'relay_ch' + ch + '=' + state,
		dataType: 'json',
		timeout: ajax_timeout,
		success: function(r) {
			if (!$.trim(r)) {
				error_notify(lang_ajax_error);
				return;
			}
			
			// Reinitialize
			elm.bootstrapToggle('destroy');
			elm.bootstrapToggle();
			
			console.log(lang_success);
			notify.update({'type': 'success', 'message': '<strong>' + lang_success + '</strong>', 'progress': 100});
		},
		complete: function() {
			preventDoubleRequests(0, true);
			haltLiveUpdate();
		},
		error: function(xhr, textStatus, errorThrown) {
			// Failed, so swap the state back
			elm.prop('checked', state ? true : false).change();
			
			// Illustrate the problem checkbox
			elm.bootstrapToggle('destroy');
			elm.bootstrapToggle({
				onstyle: 'danger',
				offstyle: 'danger'
			});
			
			preventDoubleRequests(0, true);
			haltLiveUpdate();
			
			try {
				error_notify(JSON.parse(xhr.responseText));
			}
			catch(e) {
				error_notify(textStatus);
			}
		}
	});
});

// Preset
$('#preset').on('click', function(e) {
	// Prevent double requests
	if (preventDoubleRequests(e)) {
		return;
	}
	
	// Force hold
	haltupdate = true;
	
	var notify = submit_notify('<strong>' + lang_cycling + '</strong>');
	
	$.ajax({
		type: 'POST',
		url: '/submit.php',
		data: 'preset=1',
		dataType: 'json',
		timeout: ajax_timeout,
		success: function(r) {
			if (!$.trim(r)) {
				error_notify(lang_ajax_error);
				return;
			}
			
			console.log(lang_success);
			notify.update({'type': 'success', 'progress': 100});
		},
		complete: function() {
			preventDoubleRequests(0, true);
			haltLiveUpdate();
		},
		error: function(xhr, textStatus, errorThrown) {
			preventDoubleRequests(0, true);
			haltLiveUpdate();
			
			try {
				error_notify(JSON.parse(xhr.responseText));
			}
			catch(e) {
				error_notify(textStatus);
			}
		}
	});
});

// Motor control
$('.motor_control').on('click', function(e) {
	// Prevent double requests
	if (preventDoubleRequests(e)) {
		return;
	}
	
	// Get channel from data
	var ch = $(this).data('motor_channel');
	var ch_text = ch == 1 ? lang_motor_up : lang_motor_down;
	
	var notify = submit_notify('<strong>' + lang_motor_toggle + ' ' + ch_text + '</strong>');
	
	$.ajax({
		type:'POST',
		url:'/submit.php',
		data:'motor_' + ch + '=1',
		dataType:'json',
		timeout: ajax_timeout,
		success: function(r) {
			if (!$.trim(r)) {
				error_notify(lang_ajax_error);
				return;
			}
			
			console.log(lang_success);
			notify.update({'type': 'success', 'message': '<strong>' + lang_success + '</strong>', 'progress': 100});
		},
		complete: function() {
			preventDoubleRequests(0, true);
		},
		error: function(xhr, textStatus, errorThrown) {
			preventDoubleRequests(0, true);
			
			try {
				error_notify(JSON.parse(xhr.responseText));
			}
			catch(e) {
				error_notify(textStatus);
			}
		}
	});
});

// System Reset
$('#system_reset').on('click', function() {
	bootbox.dialog({
		message: lang_reboot,
		buttons: {
			danger: {
				label: reboot_label,
				className: 'btn-danger',
				callback: function() {
					haltupdate = true;
					
					var notify = submit_notify('<strong>' + lang_rebooting + '</strong>', 120000);
					
					$.ajax({
						type: 'POST',
						url: '/submit.php',
						data: 'system_reset=1',
						dataType: 'json',
						timeout: ajax_timeout,
						success: function(r) {
							if (!$.trim(r)) {
								error_notify(lang_ajax_error);
								return;
							}
							
							console.log(lang_rebooting_inprogress);
							notify.update({'type': 'info', 'message': '<strong>' + lang_rebooting_inprogress + '</strong>'});
							
							// Wait 10 seconds before checking (optimistic, maybe with a good class 10 SD)
							setTimeout(function() {
								var count = 0;
								
								var check = setInterval(function() {
									count++;
									
									$.ajax({
										type: 'POST',
										url: '/submit.php',
										data: 'system_status=1',
										dataType: 'json',
										timeout: ajax_timeout,
										success: function(s) {
											if (!$.trim(s)) {
												error_notify(lang_ajax_error);
												return;
											}
											
											console.log(lang_rebooting_done);
											notify.update({'type': 'success', 'message': '<strong>' + lang_rebooting_done + '</strong>', 'progress': 99});
											
											preventDoubleRequests(0, true);
											haltupdate = false;
											clearInterval(check);
										}
									});
									
									if (count > 15) {
										console.log(lang_rebooting_slow);
										notify.update({'type': 'warning', 'message': '<strong>' + lang_rebooting_slow + '</strong>'});
									}
									
									if (count > 30) {
										error_notify(lang_rebooting_error);
										
										preventDoubleRequests(0, true);
										haltupdate = false;
										clearInterval(check);
									}
								}, 3000);
							}, 10000);
						},
						error: function(xhr, textStatus, errorThrown) {
							preventDoubleRequests(0, true);
							haltupdate = false;
							
							try {
								error_notify(JSON.parse(xhr.responseText));
							}
							catch(e) {
								error_notify(textStatus);
							}
						}
					});
				}
			},
			main: {
				label: lang_cancel,
				className: 'btn-default',
				callback: function() {}
			}
		}
	});
});
