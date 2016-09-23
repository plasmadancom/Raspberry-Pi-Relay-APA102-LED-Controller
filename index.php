<?php

/*
 * index.php - Web GUI front page
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

$color = GetColor();

$red = $color[0];
$green = $color[1];
$blue = $color[2];
$lux = end($color);

?>
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
		<meta name="author" content="Dan Jones">
		<!-- Page title -->
		<title><?php echo $title; ?></title>
		
		<!-- Icons -->
		<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
		<link rel="icon" type="image/png" href="/favicon-32x32.png" sizes="32x32">
		<link rel="icon" type="image/png" href="/favicon-16x16.png" sizes="16x16">
		
		<!-- Android App settings -->
		<link rel="manifest" href="/manifest.json">
		
		<!-- Apple icon mask -->
		<link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5bbad5">
		
		<!-- App theme color -->
		<meta name="theme-color" content="#444444">
        <link rel="stylesheet" href="/css/bootstrap.min.css">
		<link rel="stylesheet" href="/css/bootstrap-toggle.min.css">
		<link rel="stylesheet" href="/css/animate.min.css">
		<link rel="stylesheet" href="/css/style.css">
		<script src="/js/jquery-1.12.4.min.js"></script>
		<script src="/js/bootstrap-toggle.min.js"></script>
		<script src="/js/jquery.wheelcolorpicker.modified.js"></script>
		<script src="/js/bootstrap-notify.min.js"></script>
		<script src="/js/bootbox.min.js"></script>
		<!--[if lt IE 9]>
			<script src="/js/html5shiv.min.js"></script>
			<script src="/js/respond.min.js"></script>
		<![endif]-->
	</head>
	<body>
		<!-- placed outside of <head> due to weird bug with this plugin -->
		<link rel="stylesheet" property="stylesheet" href="/css/wheelcolorpicker.modified.css">
		
		<!-- Page settings -->
		<input id="red" type="hidden" value="<?php echo $red; ?>">
		<input id="green" type="hidden" value="<?php echo $green; ?>">
		<input id="blue" type="hidden" value="<?php echo $blue; ?>">
		<input id="lux" type="hidden" value="<?php echo $lux; ?>">
		<input id="minbrightness" type="hidden" value="<?php echo $lux_lowest; ?>">
		<input id="maxbrightness" type="hidden" value="<?php echo $lux_highest; ?>">
		<input id="autoupdate" type="hidden" value="<?php echo $autoupdate; ?>">
		<input id="ajax_timeout" type="hidden" value="<?php echo $ajax_timeout; ?>">
		<input id="refreshtimer" type="hidden" value="<?php echo $refresh_timer; ?>">
		<input id="ac_detect" type="hidden" value="<?php echo $ac_detect; ?>">
		<input id="ac_detect_port_1" type="hidden" value="<?php echo $ac_detect_port_1; ?>">
		<input id="ac_detect_port_2" type="hidden" value="<?php echo $ac_detect_port_2; ?>">
		<input id="relay_1" type="hidden" value="<?php echo $relay_1; ?>">
		<input id="relay_2" type="hidden" value="<?php echo $relay_2; ?>">
		
		<!-- Language -->
		<input id="lang_success" type="hidden" value="<?php echo $lang_success; ?>">
		<input id="lang_warning" type="hidden" value="<?php echo $lang_warning; ?>">
		<input id="lang_error" type="hidden" value="<?php echo $lang_error; ?>">
		<input id="lang_ajax_error" type="hidden" value="<?php echo $lang_ajax_error; ?>">
		<input id="lang_ajax_invalid" type="hidden" value="<?php echo $lang_ajax_invalid; ?>">
		<input id="lang_ajax_missing" type="hidden" value="<?php echo $lang_ajax_missing; ?>">
		<input id="lang_setting" type="hidden" value="<?php echo $lang_setting; ?>">
		<input id="lang_setting_color" type="hidden" value="<?php echo $lang_setting_color; ?>">
		<input id="lang_setting_brightness" type="hidden" value="<?php echo $lang_setting_brightness; ?>">
		<input id="lang_set_color_mismatch" type="hidden" value="<?php echo $lang_set_color_mismatch; ?>">
		<input id="lang_set_brightness_mismatch" type="hidden" value="<?php echo $lang_set_brightness_mismatch; ?>">
		<input id="lang_switching" type="hidden" value="<?php echo $lang_switching; ?>">
		<input id="lang_cycling" type="hidden" value="<?php echo $lang_cycling; ?>">
		<input id="lang_motor_up" type="hidden" value="<?php echo $lang_motor_up; ?>">
		<input id="lang_motor_down" type="hidden" value="<?php echo $lang_motor_down; ?>">
		<input id="lang_motor_toggle" type="hidden" value="<?php echo $lang_motor_toggle; ?>">
		<input id="lang_reboot" type="hidden" value="<?php echo $lang_reboot; ?>">
		<input id="lang_rebooting" type="hidden" value="<?php echo $lang_rebooting; ?>">
		<input id="lang_rebooting_inprogress" type="hidden" value="<?php echo $lang_rebooting_inprogress; ?>">
		<input id="lang_rebooting_slow" type="hidden" value="<?php echo $lang_rebooting_slow; ?>">
		<input id="lang_rebooting_error" type="hidden" value="<?php echo $lang_rebooting_error; ?>">
		<input id="lang_rebooting_done" type="hidden" value="<?php echo $lang_rebooting_done; ?>">
		
		<!-- Static navbar -->
		<nav class="navbar navbar-inverse navbar-static-top">
			<div class="container">
				<div class="navbar-header">
					<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
						<span class="sr-only">Toggle navigation</span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
					</button>
					<a class="navbar-brand" href="./"><?php echo $title; ?></a>
				</div>
				<div id="navbar" class="navbar-collapse collapse">
					<ul class="nav navbar-nav navbar-right">
						<!-- GitHub / AV Forums project pages, remove if you prefer :) -->
						<li><a target="_blank" href="https://github.com/plasmadancom/Raspberry-Pi-Relay-APA102-LED-Controller">GitHub</a></li>
						<li><a target="_blank" href="https://www.avforums.com/threads/ongoing-plasmadans-living-room-cinema-office-build.1992617/">AV Forums</a></li>
<?php if ($reboot_button) { ?>
						<!-- Reboot button -->
						<li><button type="button" id="system_reset" class="btn btn-danger navbar-btn"><?php echo $reboot_label; ?></button></li>
<?php } ?>
					</ul>
				</div>
			</div>
		</nav>
		
		<!-- Main -->
		<div class="container">
			<div class="row wrapper">
				<div class="col-md-6">
					<div class="row">
						<div class="col-xs-8">
							<span class="switch_label"><?php echo $relay_ch1_label; ?></span>
						</div>
						<div class="col-xs-4 text-right no_line_height">
							<label class="toggle">
								<input id="relay_ch1" class="relay_checkbox" type="checkbox" data-relay="1" data-toggle="toggle" data-size="normal"<?php if(($ac_detect && gpio_status($ac_detect_port_1)) || (!$ac_detect && gpio_status($relay_1))) echo ' checked '; ?>>
							</label>
						</div>
					</div>
<?php if ($enable_relay_ch2) { ?>
					<div class="row">
						<div class="col-xs-8">
							<span class="switch_label"><?php echo $relay_ch2_label; ?></span>
						</div>
						<div class="col-xs-4 text-right no_line_height">
							<label class="toggle">
								<input id="relay_ch2" class="relay_checkbox" type="checkbox" data-relay="2" data-toggle="toggle" data-size="normal"<?php if(($ac_detect && gpio_status($ac_detect_port_2)) || (!$ac_detect && gpio_status($relay_2))) echo ' checked '; ?>>
							</label>
						</div>
					</div>
<?php
}
if ($enable_motor_control) {
?>
					<div class="row">
						<div class="col-xs-4">
							<span class="switch_label"><?php echo $motor_label; ?></span>
						</div>
						<div class="col-xs-8 text-right">
							<button type="button" data-motor_channel="1" class="btn btn-primary motor_control"><span class="glyphicon glyphicon-chevron-up"></span></button>
							<button type="button" data-motor_channel="2" class="btn btn-primary motor_control"><span class="glyphicon glyphicon-chevron-down"></span></button>
						</div>
					</div>
<?php
}
if ($preset_button) { ?>
					<div class="row">
						<div class="col-xs-12 text-right">
							<button type="button" id="preset" class="btn btn-primary"><?php echo $preset_label; ?></button>
						</div>
					</div>
<?php } ?>
				</div>
				<div class="col-md-6">
					<div class="row">
						<div class="col-xs-12 no_line_height">
							<input class="colorpicker" type="text" data-wheelcolorpicker="" data-wcp-layout="block" data-wcp-sliders="wsl" data-wcp-autoresize="false" data-wcp-cssclass="colorpicker-size">
						</div>
					</div>
				</div>
			</div>
			<script src="/js/bootstrap.min.js"></script>
			<script src="/js/functions.js"></script>
		</div>
	</body>
</html>
