# Raspberry Pi Relay & APA102 LED Controller

![alt tag](http://img.photobucket.com/albums/v287/plasma_dan/responsive-showcase-mockup_zpsqssh3wjo.png~original)

![alt tag](/pcb-animated.gif)

Raspberry Pi Relay & APA102 LED controller allows control & switching of APA102 addressable LEDs (and LED driver) using a web GUI. Motor controller functionality is also built-in to control hard-wired home automation type blind / projector screen motors. Ideal for use in home cinema applications.

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

![alt tag](http://img.photobucket.com/albums/v287/plasma_dan/iphone6-mockup_zpsm93mbcdt.png~original)

The GUI includes controls for the changeover relay channels, motorised blind / projector screen, a full RGB color picker for the APA102 LEDs and a preset control to cycle built-in light modes / effects. There is also the ability to reboot the Raspberry Pi directly from the GUI, making development & testing easier for your application.

Built on bootstrap 3; the GUI is fully responsive and adapts to any screen size / orientation.

## App Features

As well as support for mobile devices, the GUI includes modern manifest data to allow it to work more like a native app. This means when you save the GUI to the home-screen it will load & function without an address-bar, just like an app.

## Prerequisites

Raspberry Pi with Raspian:
https://www.raspberrypi.org/downloads/raspbian/

I recommend a clean Raspian install before proceeding.

## Dependencies

APA102 LEDs require the Python port of the Adafruit DotStar library to function. This is included in this repo for completeness.

https://github.com/adafruit/Adafruit_DotStar_Pi

## Build Your Own!

The hardware for this controller is quite simple, all the components are readily available. If you decide to build one for yourself, I have provided the necessary Gerber files for the PCB. These can either be sent to a PCB manufacturer like [PCBway](http://www.pcbway.com), or you can etch the board yourself (see included transfer pdf). The PCB design is single-sided to make it easier to re-create yourself. The PCB was designed to fit into a small case ([CAMDENBOSS 7200-269C](http://camdenboss.com/enclosures/heavy-duty-enclosures/polycarbonate-clear-lid-cases#7200-series-grey-clear200x120x75)). If you require additional inputs / outputs, or want to make any other changes; you may want to create your own PCB instead.

![alt tag](/pcb-black-transfer.png)

Parts list: https://goo.gl/5SdG7h

Alternatively you can buy a PCB or complete controller from me. Contact me on AV Forums [here](https://www.avforums.com/members/plasma-dan.314603/).

## Just The Basics

If all you want is LED control via Raspberry Pi, you can do this without a PCB. The circuit diagram below shows how to connect APA102 LEDs to a Raspberry Pi using a [74AHCT125 - Quad Level-Shifter](https://www.adafruit.com/product/1787). You will still need an LED driver to power the LEDs. The LEDs must share a common-ground with the Raspberry Pi & LED driver.

![alt tag](/apa102-raspberry-pi-circuit-diagram.png)

## Stackable

The PCB can easily be stacked using standoffs. The [CAMDENBOSS 7200-269C](http://camdenboss.com/enclosures/heavy-duty-enclosures/polycarbonate-clear-lid-cases#7200-series-grey-clear200x120x75) enclosure is tall enough to accommodate two stacked boards. So if you require more channels; this is a simple solution.

## Raspberry Pi Compatibility

* All except the original Model B (rev. 1) - Although with some changes it can be made to work.

The PCB design uses a 26-way header (same as the Raspberry Pi model B). A 26-way to 40-way ribbon cable will be needed to work with Raspberry Pi B+ and above.

## Wiring

![alt tag](http://img.photobucket.com/albums/v287/plasma_dan/My%20Projects/Dads%20House/Living%20Room/2016-08-19%2016.07.03_zps45mc1tgi.jpg)

The controller is designed to work with 4-wire type addressable LED strips; such as APA102 (AKA Adafruit DotStars) or WS2801. Everything else on the controller is pretty-much universal in terms of wiring options. I have provided an example wiring diagram:

![alt tag](/example-wiring-diagram-v2.png)

In this example, the LED driver and halogen lighting circuits are linked to the changeover relay channels. This allows for standard 2-way / intermediate (3-way if you're outside the UK) light switches to be used in conjunction with the controller. This means that if the controller went offline for whatever reason, your lights will still work!

Notice in the example that the switched-line is looped back into the AC detect circuits. This is to allow the Raspberry Pi to sense when the lights / LED driver are powered, regardless of relay / switch positions. If you don't require 2-way control you can disable this in the config.

# Installation

```
sudo bash
```

Update Raspian

```
apt-get update
apt-get upgrade
```

## Install Apache components

```
apt-get install apache2 php5 libapache2-mod-php5
```

## Install WiringPi

```
apt-get install git-core -y
```

Get repo

```
git clone git://git.drogon.net/wiringPi
```

Build WiringPi

```
cd wiringPi
git pull origin
./build
```

Install python-dev  & pip

```
apt-get install python-dev python-pip -y
```

Install WiringPi

```
pip install wiringpi2
```

## Enable SPI

Needed for RGB LEDs to work.

```
raspi-config
```

Scroll to "Advanced Options", "SPI", set to enabled.

## Clone Repo Contents

```
cd /var/www/html
```

Empty default Apache files

```
rm -rf *
```

Clone repo

```
git clone https://github.com/plasmadancom/Raspberry-Pi-Relay-APA102-LED-Controller .
```

Be sure to set file permissions to 755 in the web directory.

```
chmod -R 755 /var/www
```

Apache requires sudo permission to use WiringPi.
Note: If your Raspberry Pi is on a shared network you may want to find a more secure method than this.

```
echo "www-data ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
```

To make the Python scripts run at startup, edit rc.local:

```
nano /etc/rc.local
```

Add before exit 0

```
python /var/www/html/python/motor.py&
python /var/www/html/python/preset.py&
```

The scripts are independent from each other to allow you to just use what you need.

## Optional: install vsftpd for easier file editing

```
apt-get install vsftpd -y
```

Change user for vsftpd

```
chown -R pi /var/www
```

Edit vsftpd.conf

```
nano /etc/vsftpd.conf
```

Uncomment the following line:

```
write_enable=YES
```

Add the following line:

```
force_dot_files=YES
```

Restart vsftpd

```
service vsftpd restart
```

## Config

There are lots of user customisable options in the config file :```/python/config.py```
Edit the config options as required.

## License

MIT © Dan Jones - [PlasmaDan.com](https://plasmadan.com)
