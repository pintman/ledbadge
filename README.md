# ledbadge

## ampy-fix

In order to run ampy on the wemos d1 mini you must specify --delay 0.5 on the commandline.
[Source](https://github.com/adafruit/ampy/issues/19).

    $ ampy -d 0.5 -p ... ls

