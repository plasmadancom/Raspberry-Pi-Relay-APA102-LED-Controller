# R-Pi Relay + RGB Controller

![alt tag](/PCB-photo.jpg)

Allows use of fully addressable RGB LEDs as mood lighting. Ideal for anyone who wants to implement light effects / light shows / sequences, but still retain some basic lighting control. The project uses the WiringPi library to listen for a GPIO input, allowing for sequential color cycling / color fading / dimming of the LEDs; from a single button.

Also offers a blind motor controller script; to control hard-wired home automation type blind / shutter motors from a single button. Can also be used with motorised projector screens for use in home cinema applications.

# Motivation

This project was created for use in my own home cinema build. I wanted a single-room home automation solution that would offer relay control of mains AC lighting, blind motor control and addressable RGB control in a single unit.

Home cinema build log: https://www.avforums.com/threads/ongoing-plasmadans-living-room-cinema-office-build.1992617/

## TODO

Finish the web GUI

## Prerequisites

Raspberry Pi with clean Raspian install:
https://www.raspberrypi.org/downloads/raspbian/

## Dependancies

https://github.com/WiringPi/WiringPi-Python

https://github.com/adafruit/Adafruit_DotStar_Pi

## Installation

Update Raspian

```
apt-get update
apt-get upgrade
```

Install Apache components

```
apt-get install apache2 php5 libapache2-mod-php5 mysql-server php5-mysql
```

Install vsftpd

```
apt-get install vsftpd
```

Change user for vsftpd

```
chown -R pi /var/www
```

Allow Apache permission

```
chmod -R 755 /var/www
```

Allow .htaccess files. Edit vsftpd.conf

```
nano /etc/vsftpd.conf
```

Add the following line:

```
force_dot_files=YES
```

Restart vsftpd

```
service vsftpd restart
```

Install WiringPi

Follow their guide here: https://github.com/WiringPi/WiringPi-Python

## Usage

Edit the config options in color.py / motor.py as required.

FTP into the Pi and transfer your modified scripts to ```/var/www/html/Python```, or choose your own location. Be sure to set file permissions to 755 in the web directory.

To make the scripts run at startup, edit rc.local:

```
nano /etc/rc.local
```

Add before exit 0

```
python /var/www/html/python/motor.py&
python /var/www/html/python/color.py&
```

Alter the paths as required. The scripts are independent from each other to allow you to just use what you need.

## License

MIT © [Dan Jones](https://www.danielkeithjones.com) - [PlasmaDan.com](https://plasmadan.com)
