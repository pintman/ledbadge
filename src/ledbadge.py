import time
import tm1640
from machine import Pin
import math
import urandom
import font

# TODO add text output
# use font.h from blinkenrocket/firmware
# https://github.com/blinkenrocket/firmware/blob/cd32abec64bd5c5d1606c54272d91b39328efff6/src/font.h
# format: First: number of columns, following bit representation of char
"""
eight = [0x05,0x36,0x49,0x49,0x49,0x36]
at = [0x07,0x3E,0x41,0x49,0x55,0x5D,0x45,0x38]
x = [0x05,0x11,0x0A,0x04,0x0A,0x11]
space = [0x03,0x00,0x00,0x00]
excl =[0x01,0x7D]
bigA = [0x05,0x3F,0x48,0x48,0x48,0x3F]

for sign in [eight, x, space, excl, bigA]:
    for ch in sign:
        s = bin(ch)[2:]
        s = s.zfill(8)
        s = s.replace("0", " ")
        s = s.replace("1", ".")
        print(s, ch)

    print()

"""


class LedMatrix:
    def __init__(self):
        self.width = 8
        self.height = 8
        self.tm = tm1640.TM1640(clk=Pin(14), dio=Pin(13))
        self._buffer = [0] * 8

    def px(self, x, y, val):
        assert 0 <= x <= self.width
        assert 0 <= y <= self.height

        if val:
            self._buffer[y] = self._buffer[y] | 2**x
        else:
            self._buffer[y] = self._buffer[y] & ~(2**x)

    def show(self):
        self.tm.write(self._buffer)

    def scroll(self, fill=0):
        """Scroll content and fill with the given byte."""
        self._buffer = self._buffer[:-1]
        self._buffer = [0] + self._buffer
        self._buffer[0] = fill


class TextScroller:
    def __init__(self, matrix):
        self.matrix = matrix

    def scroll_text(self, text, wait_time=0.08):
        """Scroll text with wait_time seconds between updates."""
        for ch in text:
            ascii_ch = ord(ch)
            # first entry contains length - ignoring this
            data = font.char[ascii_ch][1:]

            for dat in data:
                # replace last entry after scroll
                self.matrix.scroll(fill=dat)
                self.matrix.show()

                time.sleep(wait_time)

            self.matrix.scroll()  # add some extra space


class DemoBase:
    def __init__(self, ledmatrix):
        self.matrix = ledmatrix

    def run(self):
        while True:
            self.prepare()
            for x in range(self.matrix.width):
                for y in range(self.matrix.height):
                    val = self.handle_px(x, y)
                    self.matrix.px(x, y, val)
            self.matrix.show()
            time.sleep(0.01)


class PlasmaDemo(DemoBase):
    """Plasma"""
    def __init__(self, ledmatrix):
        super().__init__(ledmatrix)
        self.i = 0
        self.s = 1

    def prepare(self):
        self.i += 2
        self.s = math.sin(self.i / 50.0) * 2.0 + 6.0

    def handle_px(self, x, y):
        v = 0.3 + (0.3 * math.sin((x * self.s) + self.i / 4.0) *
                   math.cos((y * self.s) + self.i / 4.0))
        return v > 0.3


class RotatingPlasmaDemo(DemoBase):
    """Rotating Plasma"""
    def __init__(self, flipdotdisplay):
        super().__init__(flipdotdisplay)
        self.current = time.ticks_us() / 1000000

    def prepare(self):
        self.current = time.ticks_us() / 1000000

    def handle_px(self, x, y):
        v = math.sin(3 * (0.5 * x * math.sin(self.current / 2) +
                     0.5 * y * math.cos(self.current / 3)) + self.current)
        # -1 < sin() < +1
        # therfore correct the value and bring into range [0, 1]
        v = (v + 1.0) / 2.0
        return v > 0.5


class GameOfLife(DemoBase):
    """Conway's Game of Life"""

    glider = {
        (2, 2),
        (1, 2),
        (0, 2),
        (2, 1),
        (1, 0),
    }

    MAX_ITERATIONS = 100

    def __init__(self, ledmatrix):
        super().__init__(ledmatrix)
        # self.cells = GameOfLife.glider
        self.cells = set()
        self.iterations = 0
        self.reset()

    def reset(self):
        self.iterations = 0
        for i in range(self.matrix.width * self.matrix.height // 2):
            x = urandom.getrandbits(3)
            y = urandom.getrandbits(3)
            # x = random.randint(0, self.fdd.width - 1)
            # y = random.randint(0, self.fdd.height - 1)
            self.cells.add((x, y))
        print("generated", len(self.cells), "cells")

    def _iterate(self):
        new_board = set()
        for cell in self.cells:
            neighbours = self._neighbours(cell)
            if len(self.cells.intersection(neighbours)) in (2, 3):
                new_board.add(cell)
            for nb in neighbours:
                if len(self.cells.intersection(self._neighbours(nb))) == 3:
                    new_board.add(nb)

        return new_board

    def _neighbours(self, cell):
        x, y = cell
        r = range(-1, 2)  # -1, 0, +1
        return set((x + i, y + j) for i in r for j in r if not i == j == 0)

    def prepare(self):
        self.cells = self._iterate()
        self.iterations += 1
        if len(self.cells) == 0 or self.iterations > GameOfLife.MAX_ITERATIONS:
            print("resetting game")
            self.reset()

    def handle_px(self, x, y):
        return (x, y) in self.cells


class PingPong(DemoBase):
    """PingPong Demo"""
    def __init__(self, ledmatrix):
        super().__init__(ledmatrix)
        self.vel = [1, 1]
        self.pos = [0, self.matrix.height // 2]

    def handle_px(self, x, y):
        if x == self.pos[0] and y == self.pos[1]:
            return True
        else:
            return False

    def prepare(self):
        if self.pos[0] + self.vel[0] > self.matrix.width or \
                self.pos[0] + self.vel[0] < 0:
            self.vel[0] = -self.vel[0]

        if self.pos[1] + self.vel[1] > self.matrix.height or \
                self.pos[1] + self.vel[1] < 0:
            self.vel[1] = -self.vel[1]

        self.pos = [self.pos[0] + self.vel[0],
                    self.pos[1] + self.vel[1]]


def run_pingpong_demo():
    mat = LedMatrix()
    PingPong(mat).run()


def run_rotating_plasma():
    RotatingPlasmaDemo(LedMatrix()).run()


def testmatrix():
    matrix = LedMatrix()
    print("all off")
    for y in range(matrix.height):
        for x in range(matrix.width):
            matrix.px(x, y, False)
    matrix.show()
    time.sleep(0.3)

    print("all on")
    for y in range(matrix.height):
        for x in range(matrix.width):
            matrix.px(x, y, True)
            matrix.show()
            time.sleep(0.1)

    print("every other on")
    for y in range(matrix.height):
        for x in range(matrix.width):
            matrix.px(x, y, x % 2 == 0)
            matrix.show()
            time.sleep(0.1)


def flicker():
    print("flickering the display as fast as possible")
    matrix = LedMatrix()
    for i in range(10):
        matrix.tm.write([0] * 8)
        matrix.tm.write([255] * 8)


def run_game_of_life():
    mat = LedMatrix()
    gol = GameOfLife(mat)
    gol.run()


def run_plasma_demo():
    PlasmaDemo(LedMatrix()).run()


def test_text_scroller():
    TextScroller(LedMatrix()).scroll_text("hallo welt 42!")


def main():
    print("starting in some seconds")
    time.sleep(1)
    print("starting led badge")

    TextScroller(LedMatrix()).scroll_text("It's demo time... :) ...   ")
    # test_text_scroller()
    run_rotating_plasma()
    #run_pingpong_demo()
    #run_game_of_life()
    #run_plasma_demo()
