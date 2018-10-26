import tm1640
from machine import Pin
import text


class LedMatrix:
    def __init__(self, border_length=8, clkpin=14, diopin=13):
        self.width = border_length
        self.height = border_length
        self.border_length = border_length
        self.tm = tm1640.TM1640(clk=Pin(clkpin), dio=Pin(diopin))
        self._buffer = [0] * border_length

    def px(self, x, y, val):
        '''
        Set pixel at x,y to be on or off. Needs invocation of show() 
        afterwards.
        '''
        assert 0 <= x <= self.width
        assert 0 <= y <= self.height

        if val:
            self._buffer[y] = self._buffer[y] | 2**x
        else:
            self._buffer[y] = self._buffer[y] & ~(2**x)

    def write_char(self, char):
        'Write character to buffer. Needs invocation of show() afterwards.'
        buf = text.buffer_for_char(char)
        # fill with zeros
        gap = (self.border_length - len(buf)) * [0]
        self._buffer = buf + gap

    def show(self):
        'Show the current buffer on the display.'
        self.tm.write(self._buffer)

    def scroll(self, fill=0):
        'Scroll content and fill with the given byte.'
        self._buffer = [fill] + self._buffer[:-1]

    def clear(self):
        'Clear the matrix screen buffer.'
        self._buffer = [0] * 8
