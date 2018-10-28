import time

import utaskmanager

# taken from
# https://github.com/blinkenrocket/firmware/tree/master/src/font.h
# format: bit representation of character, column by column
#
_font = {}
_font[32] = [0x00, 0x00, 0x00]  # <space>
_font[33] = [0x7D]  # !
_font[34] = [0x30, 0x40, 0x30, 0x40]  # "
_font[35] = [0x12, 0x3F, 0x12, 0x12, 0x3F, 0x12]  #  #
_font[36] = [0x12, 0x2A, 0x7F, 0x2A, 0x24]  # $
_font[37] = [0x30, 0x4A, 0x34, 0x08, 0x16, 0x29, 0x06]  # %
_font[38] = [0x36, 0x49, 0x49, 0x49, 0x27]  # &
_font[39] = [0x70]  # '
_font[40] = [0x1C, 0x22, 0x41]  # (
_font[41] = [0x41, 0x22, 0x1C]  # )
_font[42] = [0x28, 0x10, 0x7C, 0x10, 0x28]  # *
_font[43] = [0x08, 0x08, 0x3E, 0x08, 0x08]  # +
_font[44] = [0x01, 0x02]  # ,
_font[45] = [0x08, 0x08, 0x08, 0x08, 0x08]  # -
_font[46] = [0x01]  # .
_font[47] = [0x03, 0x1C, 0x60]  # /
_font[48] = [0x3E, 0x45, 0x49, 0x51, 0x3E]  # 0
_font[49] = [0x10, 0x20, 0x7F]  # 1
_font[50] = [0x21, 0x43, 0x45, 0x49, 0x31]  # 2
_font[51] = [0x22, 0x41, 0x49, 0x49, 0x36]  # 3
_font[52] = [0x0C, 0x14, 0x24, 0x44, 0x7F]  # 4
_font[53] = [0x72, 0x51, 0x51, 0x51, 0x4E]  # 5
_font[54] = [0x3E, 0x49, 0x49, 0x49, 0x26]  # 6
_font[55] = [0x43, 0x44, 0x48, 0x50, 0x60]  # 7
_font[56] = [0x36, 0x49, 0x49, 0x49, 0x36]  # 8
_font[57] = [0x32, 0x49, 0x49, 0x49, 0x3E]  # 9
_font[58] = [0x12]  # :
_font[59] = [0x01, 0x12]  # ;
_font[60] = [0x08, 0x14, 0x22]  # <
_font[61] = [0x14, 0x14, 0x14, 0x14, 0x14]  # =
_font[62] = [0x22, 0x14, 0x08]  # >
_font[63] = [0x20, 0x40, 0x45, 0x48, 0x30]  # ?
_font[64] = [0x3E, 0x41, 0x49, 0x55, 0x5D, 0x45, 0x38]  # @
_font[65] = [0x3F, 0x48, 0x48, 0x48, 0x3F]  # A
_font[66] = [0x7F, 0x49, 0x49, 0x49, 0x36]  # B
_font[67] = [0x3E, 0x41, 0x41, 0x41, 0x22]  # C
_font[68] = [0x7F, 0x41, 0x41, 0x41, 0x3E]  # D
_font[69] = [0x7F, 0x49, 0x49, 0x41, 0x41]  # E
_font[70] = [0x7F, 0x48, 0x48, 0x40, 0x40]  # F
_font[71] = [0x3E, 0x41, 0x41, 0x49, 0x2F]  # G
_font[72] = [0x7F, 0x08, 0x08, 0x08, 0x7F]  # H
_font[73] = [0x7F]  # I
_font[74] = [0x02, 0x01, 0x01, 0x01, 0x7E]  # J
_font[75] = [0x7F, 0x08, 0x14, 0x22, 0x41]  # K
_font[76] = [0x7F, 0x01, 0x01, 0x01, 0x01]  # L
_font[77] = [0x7F, 0x10, 0x08, 0x04, 0x08, 0x10, 0x7F]  # M
_font[78] = [0x7F, 0x10, 0x08, 0x04, 0x7F]  # N
_font[79] = [0x3E, 0x41, 0x41, 0x41, 0x3E]  # O
_font[80] = [0x7F, 0x48, 0x48, 0x48, 0x30]  # P
_font[81] = [0x3E, 0x41, 0x45, 0x42, 0x3D]  # Q
_font[82] = [0x7F, 0x44, 0x44, 0x46, 0x39]  # R
_font[83] = [0x32, 0x49, 0x49, 0x49, 0x26]  # S
_font[84] = [0x40, 0x40, 0x7F, 0x40, 0x40]  # T
_font[85] = [0x7E, 0x01, 0x01, 0x01, 0x7E]  # U
_font[86] = [0x7C, 0x02, 0x01, 0x02, 0x7C]  # V
_font[87] = [0x7E, 0x01, 0x01, 0x1E, 0x01, 0x01, 0x7E]  # W
_font[88] = [0x63, 0x14, 0x08, 0x14, 0x63]  # X
_font[89] = [0x60, 0x10, 0x0F, 0x10, 0x60]  # Y
_font[90] = [0x43, 0x45, 0x49, 0x51, 0x61]  # Z
_font[91] = [0x7F, 0x41, 0x41]  # [
_font[92] = [0x60, 0x1C, 0x03]  # backslash
_font[93] = [0x41, 0x41, 0x7F]  # ]
_font[94] = [0x10, 0x20, 0x40, 0x20, 0x10]  # ^
_font[95] = [0x01, 0x01, 0x01, 0x01, 0x01]  # _
_font[96] = [0x40, 0x20]  # `
_font[97] = [0x02, 0x15, 0x15, 0x15, 0x0F]  # a
_font[98] = [0x7F, 0x11, 0x11, 0x11, 0x0E]  # b
_font[99] = [0x0E, 0x11, 0x11, 0x11, 0x0A]  # c
_font[100] = [0x0E, 0x11, 0x11, 0x11, 0x7F]  # d
_font[101] = [0x0E, 0x15, 0x15, 0x15, 0x0C]  # e
_font[102] = [0x10, 0x3F, 0x50, 0x50, 0x40]  # f
_font[103] = [0x08, 0x15, 0x15, 0x15, 0x1E]  # g
_font[104] = [0x7F, 0x10, 0x10, 0x10, 0x0F]  # h
_font[105] = [0x5F]  # i
_font[106] = [0x02, 0x01, 0x01, 0x01, 0x5E]  # j
_font[107] = [0x7F, 0x04, 0x0C, 0x12, 0x01]  # k
_font[108] = [0x7F]  # l
_font[109] = [0x1F, 0x10, 0x10, 0x0C, 0x10, 0x10, 0x0F]  # m
_font[110] = [0x1F, 0x10, 0x10, 0x10, 0x0F]  # n
_font[111] = [0x0E, 0x11, 0x11, 0x11, 0x0E]  # o
_font[112] = [0x0F, 0x14, 0x14, 0x14, 0x08]  # p
_font[113] = [0x08, 0x14, 0x14, 0x14, 0x0F]  # q
_font[114] = [0x1F, 0x04, 0x08, 0x10, 0x10]  # r
_font[115] = [0x09, 0x15, 0x15, 0x15, 0x02]  # s
_font[116] = [0x10, 0x3E, 0x11, 0x11, 0x01]  # t
_font[117] = [0x1E, 0x01, 0x01, 0x01, 0x1E]  # u
_font[118] = [0x1C, 0x02, 0x01, 0x02, 0x1C]  # v
_font[119] = [0x1E, 0x01, 0x01, 0x02, 0x01, 0x01, 0x1E]  # w
_font[120] = [0x11, 0x0A, 0x04, 0x0A, 0x11]  # x
_font[121] = [0x19, 0x05, 0x05, 0x05, 0x1E]  # y
_font[122] = [0x11, 0x13, 0x15, 0x19, 0x11]  # z
_font[123] = [0x08, 0x36, 0x41, 0x41]  # [
_font[124] = [0x7F]  # |
_font[125] = [0x41, 0x41, 0x36, 0x08]  # ]
_font[126] = [0x20, 0x40, 0x40, 0x20, 0x20, 0x40]  # ~


class TextScroller:
    def __init__(self, matrix):
        self.matrix = matrix

    def scroll_text(self, text, wait_time=0.08):
        """Scroll text with wait_time seconds between updates."""
        for ch in text:
            ascii_ch = ord(ch)

            for dat in _font[ascii_ch]:
                self.matrix.scroll(fill=dat)
                self.matrix.show()
                time.sleep(wait_time)

            self.matrix.scroll()  # add some extra space


class TextScrollerTask(utaskmanager.Task):
    def __init__(self, matrix):
        super().__init__()
        self.matrix = matrix
        self.textbuffer = []
        self.current_index = 0
        self._paused = False

    def pause(self, is_paused):
        '''
        set the scroller in paused mode or not. In paused mode, the 
        display will not be updated
        '''
        self._paused = is_paused

    def set_text(self, new_text):
        'change the currently shown text.'
        self.textbuffer = []
        for ch in new_text:
            line = buffer_for_char(ch) + [0x00]
            self.textbuffer.extend(line)

    def task_step(self):
        if self._paused or len(self.textbuffer) == 0:
            return

        current_line = self.textbuffer[self.current_index]
        self.matrix.scroll(fill=current_line)
        self.current_index = (self.current_index + 1) % len(self.textbuffer)
        self.matrix.show()


def buffer_for_char(char):
    return _font[ord(char)]
