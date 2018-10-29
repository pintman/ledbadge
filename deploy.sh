#!/bin/bash

FILES="*.py"
BIG_FILES="text.py main.py"
AMPY_PORT=/dev/ttyUSB0

for f in $FILES; do
    echo "$f -> ESP"
    ampy -p ${AMPY_PORT} put $f
done

for f in $BIG_FILES; do
    echo "$f: cross compiling"
    python -m mpy_cross ${f}
    echo "  removing from ESP "
    ampy -p ${AMPY_PORT} rm ${f}
    echo "  putting compiled version to ESP "
    ampy -p ${AMPY_PORT} put $(basename ${f} .py).mpy
done
