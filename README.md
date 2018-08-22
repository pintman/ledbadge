# ledbadge

## Installation

For tools run

    $ pip3 install -r requirements.txt

For testing and runnning in a local micropython environment install 
the upython packages with

	$ micropython -m upip install -r urequirements.txt

Currently upip does not work as intended due to an TLS
[issue](https://github.com/micropython/micropython-lib/issues/69).

## ampy-fix

In order to run ampy on the wemos d1 mini you must specify --delay 0.5 on the commandline.
[Source](https://github.com/adafruit/ampy/issues/19).

    $ ampy -d 0.5 -p ... ls

