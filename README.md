![php 5.4+](https://img.shields.io/badge/php-v5.4%2B-blue) [![maintained](https://img.shields.io/badge/maintained-yes-green.svg)](https://github.com/plasmadancom/Raspberry-Pi-Relay-APA102-LED-Controller/graphs/commit-activity) ![licence](https://img.shields.io/github/license/plasmadancom/Raspberry-Pi-Relay-APA102-LED-Controller)


# Raspberry Pi Relay & APA102 LED Controller

![APA102 LED Controller Responsive Web GUI Mockup](/img/responsive-showcase-mockup.jpg)

Raspberry Pi Relay & APA102 LED controller allows control & switching of APA102 addressable LED strips (and LED driver) using a web GUI. Motor controller functionality is also built-in to control hard-wired home automation type blind / projector screen motors. Ideal for use in home cinema applications. Unlike regular "dumb" RGB strips, addressable strips have independently controlled LEDs, allowing for the creation of light effects & sequences.

![Home Cinema Rainbow Rotate RGB LED Effect](/img/rainbow-rgb-led-soffit-lighting.jpg)

## Features

* APA102 LED control
* 2x changeover relay control
* 2x mains AC input detection
* Motorised blind / projector screen control
* 2x TTL inputs for external buttons

## Motivation

This project was created for use in my own home cinema build. I wanted a single-room home automation solution that would offer addressable RGB control, with the ability to directly switch a mains AC powered LED driver. Additional relay channels where added to the prototype to allow other circuits to be switched using the controller, such as spotlights. The motorised blind control relays were added into the design during my home cinema build.

Home cinema build log: https://www.avforums.com/threads/ongoing-plasmadans-living-room-cinema-office-build.1992617/

## Responsive Web GUI

![APA102 LED Controller iPhone6 Web GUI Mockup](/img/iphone6-mockup.jpg)

The GUI includes controls for the changeover relay channels, motorised blind / projector screen, a full RGB color picker for the APA102 LEDs and a preset control to cycle built-in light modes / effects. There is also the ability to reboot the Raspberry Pi directly from the GUI, making development & testing easier for your application.

Built on bootstrap 3; the GUI is fully responsive and adapts to any screen size / orientation.

## App Features

As well as support for mobile devices, the GUI includes modern manifest data to allow it to work more like a native app. This means when you save the GUI to the home-screen it will load & function without an address-bar, just like an app.

## Chrome Extension

The specially created Chrome extension makes the web GUI even easier to use on desktop, allowing for GUI control without the need to leave the current web page. The Chrome extension also provides the ability to map keyboard shortcuts to each function of the web GUI,  including toggle on / off, LED preset & blind control.

https://chrome.google.com/webstore/detail/apa102-led-controller/jnmjhaaahpdapgcddlgaldjhapmoapje

## Prerequisites

Raspberry Pi with Raspberry Pi OS:
https://www.raspberrypi.org/downloads/raspberry-pi-os/

I recommend a clean install before proceeding.

## Dependencies

APA102 LEDs require the Python port of the Adafruit DotStar library to function. This is included in this repo for completeness.

https://github.com/adafruit/Adafruit_DotStar_Pi

## Build Your Own!

![APA102 LED Controller PCB Animated](/img/pcb-animated.gif)

The hardware for this controller is quite simple, all the components are readily available. If you decide to build one for yourself, I have provided the necessary Gerber files for the PCB. These can either be sent to a PCB manufacturer like [PCBway](http://www.pcbway.com/setinvite.aspx?inviteid=19024), or you can etch the board yourself (see included transfer pdf). The PCB design is single-sided to make it easier to re-create yourself. The PCB was designed to fit into a small case ([CAMDENBOSS 7200-269C](http://camdenboss.com/enclosures/heavy-duty-enclosures/polycarbonate-clear-lid-cases#7200-series-grey-clear200x120x75)). If you require additional inputs / outputs, or want to make any other changes; you may want to create your own PCB instead.

![APA102 LED Controller PCB Transfer](/img/pcb-black-transfer.png)

Parts list: https://goo.gl/5SdG7h

## Raspberry Pi Compatibility

* All except the original Model B (rev. 1) - Although with some changes it can be made to work.

The PCB design uses a 26-way header (same as the Raspberry Pi model B). A 26-way to 40-way ribbon cable will be needed to work with Raspberry Pi B+ and above.

## Wiring

![APA102 LED Controller Wired](/img/Installation-example.jpg)

The controller is designed to work with 4-wire type addressable LED strips; such as APA102 (AKA Adafruit DotStars) or WS2801. Everything else on the controller is pretty-much universal in terms of wiring options. I have provided an example wiring diagram:

![APA102 LED Controller Wiring Diagram Example](/img/example-wiring-diagram-v2.png)

In this example, the LED driver and halogen lighting circuits are linked to the changeover relay channels. This allows for standard 2-way / intermediate (3-way if you're outside the UK) light switches to be used in conjunction with the controller. This means that if the controller went offline for whatever reason, your lights will still work!

Notice in the example that the switched-line is looped back into the AC detect circuits. This is to allow the Raspberry Pi to sense when the lights / LED driver are powered, regardless of relay / switch positions. If you don't require 2-way control you can disable this in the config.

# Installation

Tip: For headless setup, SSH can be enabled by placing a file named 'ssh' (no extension) onto the boot partition of the SD card.

Update your Raspberry Pi to ensure all the latest packages are installed.

```
sudo apt update
sudo apt upgrade
```

## Install Apache & PHP

```
sudo apt install apache2 php libapache2-mod-php -y
```

Test the webserver is working. Navigate to http://localhost/ on the Pi itself, or http://192.168.1.10 (whatever the Pi's IP address is) from another computer on the network. Use the snippet below to get the Pi's IP address in command line.

```
hostname -I
```

## Install WiringPi

```
sudo apt install wiringpi python-pip -y
sudo pip install wiringpi
```

## Enable SPI

Needed for RGB LEDs to work.

```
sudo raspi-config
```

Scroll to "Advanced Options", "SPI", set to enabled.

## Install GUI

You need to clone the web GUI files from the `/gui` subdirectory, to do that we need to install subversion.

```
sudo apt install subversion -y
```

Empty default Apache files and install GUI.

```
sudo rm -rf /var/www/html/*
sudo svn checkout https://github.com/plasmadancom/Raspberry-Pi-Relay-APA102-LED-Controller/trunk/gui /var/www/html
```

### Permissions

Be sure to set file permissions to 755 in the web directory.

```
sudo chmod -R 755 /var/www
```

Before proceeding, make sure the required scripts run correctly without issue.

```
python python/preset.py
```

You should see "Preset Button Control Loaded!". Do the same test for motor.py if you require it.

```
python python/motor.py
```

You should see "Motor Button Control Loaded!".

Assuming no issues, set these scripts to run automatically at startup.

Edit rc.local:

```
sudo nano /etc/rc.local
```

Add before exit 0

```
python /var/www/html/python/motor.py &
python /var/www/html/python/preset.py &
```

The scripts are independent from each other to allow you to just use what you need.

## Optional: Install vsftpd for Easier File Editing

```
sudo apt install vsftpd -y
```

Change user for vsftpd.

```
sudo chown -R pi /var/www
```

Edit vsftpd.conf.

```
sudo nano /etc/vsftpd.conf
```

Uncomment the following line:

```
write_enable=YES
```

Add the following line:

```
force_dot_files=YES
```

Save and exit nano, then restart vsftpd.

```
sudo service vsftpd restart
```

You should now be able to login via FTP.

## Config

There are lots of user customisable options in the config file :```/python/config.py```

You can customise everything from the GPIO channels used, the layout & language of the web GUI, lighting transition effects, preset modes, button timing and a whole lot more. Get familiar with the config file.

## Automation

To automate blind control actions there are 2 scripts included:

```
/python/motor_up.py
/python/motor_down.py
```

These scripts simulate a button press for up & down actions. You can use crontab to automatically trigger these scripts at a time of your choosing.

Run crontab with the -e flag to edit the cron table:

```
crontab -e
```

The first time you run crontab you'll be prompted to select an editor; if you are not sure which one to use, choose nano by pressing Enter.

Add your scheduled tasks. For help see here: https://www.raspberrypi.org/documentation/linux/usage/cron.md

For example, to schedule the blind to open at 7AM and close again at 6:30PM every day you would enter the following:

```
0 7 * * * python /var/www/html/python/motor_up.py
30 18 * * * python /var/www/html/python/motor_down.py
```

## License

MIT © Dan Jones - [PlasmaDan.com](https://plasmadan.com)
