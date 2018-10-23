from machine import Pin
import time

# GPIO pin numbers
D0 = 16
D1 = 5
D2 = 4
D3 = 0
D4 = 2
D6 = 12
D8 = 15

pins = [
    Pin(D8, mode=Pin.IN, pull=Pin.PULL_UP),
    Pin(D1, mode=Pin.IN, pull=Pin.PULL_UP),
    Pin(D2, mode=Pin.IN, pull=Pin.PULL_UP),
    Pin(D3, mode=Pin.IN, pull=Pin.PULL_UP),
    Pin(D4, mode=Pin.IN, pull=Pin.PULL_UP),
]


def main():
    print("Running pin test")
    while True:
        s = ''
        for p in pins:
            s += str(p.value()) + ' '

        print(s)

        time.sleep(0.5)
