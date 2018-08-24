# ledbadge

## Installation

### Setup the ESP

1. Download [firmware](https://micropython.org/download/#esp8266).
2. [Install](http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html#deploying-the-firmware) firmware 

### Install development tools

For tools run

    $ pip3 install -r requirements.txt

### fix for ampy

In order to run ampy on the *Wemos D1 mini* you must specify the
parameter ``--delay 0.5``` on the commandline.
[Source](https://github.com/adafruit/ampy/issues/19).

    $ ampy -d 0.5 -p ... ls


### (optional) Install development environment

For testing and runnning in a local micropython environment install 
the upython packages with

	$ micropython -m upip install -r urequirements.txt


