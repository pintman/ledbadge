from machine import Pin


class Joystick:
    def __init__(self, w, a, s, d, btn):
        'create joystick with given pins for directions and button.'

        self.directions = {'w': w, 'a': a, 's': s, 'd': d}
        for pin in self.directions.values():
            assert isinstance(pin, Pin)

        assert isinstance(btn, Pin)
        self.btn = btn

    def btn_pressed(self):
        'Return whether button is pressed.'
        return self.btn.value() == 0

    def direction(self):
        'get the current direction. One of w, a, s, d or None.'

        for wasd in self.directions:
            if self.directions[wasd].value() == 0:
                return wasd

        # no pressed direction found
        return None


# GPIO pin numbers
D0 = 16
D1 = 5
D2 = 4
D3 = 0
D4 = 2
# D6 = 12
# D8 = 15

joy = Joystick(
    w=Pin(D0, mode=Pin.IN),
    a=Pin(D1, mode=Pin.IN, pull=Pin.PULL_UP),
    s=Pin(D2, mode=Pin.IN, pull=Pin.PULL_UP),
    d=Pin(D4, mode=Pin.IN, pull=Pin.PULL_UP),
    btn=Pin(D3, mode=Pin.IN, pull=Pin.PULL_UP)
)
