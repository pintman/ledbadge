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


# GPIO pin numbers (https://wiki.wemos.cc/products:d1:d1_mini)
_D = [16, 5, 4, 0, 2, 14, 12, 13, 15]

joy = Joystick(
    # no pull up for D0 allowed. Needs external pull-up
    w=Pin(_D[0], mode=Pin.IN),
    a=Pin(_D[1], mode=Pin.IN, pull=Pin.PULL_UP),
    s=Pin(_D[2], mode=Pin.IN, pull=Pin.PULL_UP),
    d=Pin(_D[4], mode=Pin.IN, pull=Pin.PULL_UP),
    btn=Pin(_D[3], mode=Pin.IN, pull=Pin.PULL_UP)
)
