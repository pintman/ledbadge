import tm1640
from machine import Pin


class LedMatrix:
    def __init__(self):
        self.width = 8
        self.height = 8
        self.tm = tm1640.TM1640(clk=Pin(14), dio=Pin(13))
        self._buffer = [0] * 8

    def px(self, x, y, val):
        'Set pixel at x,y to be on or off. Needs invocation of show afterwards.'
        assert 0 <= x <= self.width
        assert 0 <= y <= self.height

        if val:
            self._buffer[y] = self._buffer[y] | 2**x
        else:
            self._buffer[y] = self._buffer[y] & ~(2**x)

    def show(self):
        'Show the current buffer on the display.'
        self.tm.write(self._buffer)

    def scroll(self, fill=0):
        'Scroll content and fill with the given byte.'
        self._buffer = [fill] + self._buffer[:-1]

    def clear(self):
        'Clear the matrix screen buffer.'
        self._buffer = [0] * 8
