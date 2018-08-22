# ledbadge

## Installation

For tools run

    $ pip3 install -r requirements.txt

For testing and runnning in a local micropython environment install 
the upython packages with

	$ micropython -m upip install -r urequirements.txt

## ampy-fix

In order to run ampy on the wemos d1 mini you must specify --delay 0.5 on the commandline.
[Source](https://github.com/adafruit/ampy/issues/19).

    $ ampy -d 0.5 -p ... ls

