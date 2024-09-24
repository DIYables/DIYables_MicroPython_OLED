"""
This MicroPython library is designed for any hardware plaform that supports MicroPython such as Raspberry Pi Pico, ESP32, Micro:bit... to work with the OLED display. It is created by DIYables to work with DIYables OLED display, but also work with other brand's OLED display. Please consider purchasing products from DIYables to support our work.

Product Link:
- [OLED 128x64](https://diyables.io/products/oled-128x64)
- [OLED 128x32](https://diyables.io/products/oled-128x32)


Copyright (c) 2024, DIYables.io. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

- Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.

- Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.

- Neither the name of the DIYables.io nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY DIYABLES.IO "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL DIYABLES.IO BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

from machine import I2C, Pin
import time

basic_font = [
    [0x00, 0x00, 0x00, 0x00, 0x00],  # 20 (space)
    [0x00, 0x00, 0x5F, 0x00, 0x00],  # 21 !
    [0x00, 0x07, 0x00, 0x07, 0x00],  # 22 "
    [0x14, 0x7F, 0x14, 0x7F, 0x14],  # 23 #
    [0x24, 0x2A, 0x7F, 0x2A, 0x12],  # 24 $
    [0x23, 0x13, 0x08, 0x64, 0x62],  # 25 %
    [0x36, 0x49, 0x55, 0x22, 0x50],  # 26 &
    [0x00, 0x05, 0x03, 0x00, 0x00],  # 27 '
    [0x00, 0x1C, 0x22, 0x41, 0x00],  # 28 (
    [0x00, 0x41, 0x22, 0x1C, 0x00],  # 29 )
    [0x14, 0x08, 0x3E, 0x08, 0x14],  # 2A *
    [0x08, 0x08, 0x3E, 0x08, 0x08],  # 2B +
    [0x00, 0x50, 0x30, 0x00, 0x00],  # 2C ,
    [0x08, 0x08, 0x08, 0x08, 0x08],  # 2D -
    [0x00, 0x60, 0x60, 0x00, 0x00],  # 2E .
    [0x20, 0x10, 0x08, 0x04, 0x02],  # 2F /
    [0x3E, 0x51, 0x49, 0x45, 0x3E],  # 30 0
    [0x00, 0x42, 0x7F, 0x40, 0x00],  # 31 1
    [0x42, 0x61, 0x51, 0x49, 0x46],  # 32 2
    [0x21, 0x41, 0x45, 0x4B, 0x31],  # 33 3
    [0x18, 0x14, 0x12, 0x7F, 0x10],  # 34 4
    [0x27, 0x45, 0x45, 0x45, 0x39],  # 35 5
    [0x3C, 0x4A, 0x49, 0x49, 0x30],  # 36 6
    [0x01, 0x71, 0x09, 0x05, 0x03],  # 37 7
    [0x36, 0x49, 0x49, 0x49, 0x36],  # 38 8
    [0x06, 0x49, 0x49, 0x29, 0x1E],  # 39 9
    [0x00, 0x36, 0x36, 0x00, 0x00],  # 3A :
    [0x00, 0x56, 0x36, 0x00, 0x00],  # 3B ;
    [0x08, 0x14, 0x22, 0x41, 0x00],  # 3C <
    [0x14, 0x14, 0x14, 0x14, 0x14],  # 3D =
    [0x00, 0x41, 0x22, 0x14, 0x08],  # 3E >
    [0x02, 0x01, 0x51, 0x09, 0x06],  # 3F ?
    [0x32, 0x49, 0x79, 0x41, 0x3E],  # 40 @
    [0x7E, 0x11, 0x11, 0x11, 0x7E],  # 41 A
    [0x7F, 0x49, 0x49, 0x49, 0x36],  # 42 B
    [0x3E, 0x41, 0x41, 0x41, 0x22],  # 43 C
    [0x7F, 0x41, 0x41, 0x22, 0x1C],  # 44 D
    [0x7F, 0x49, 0x49, 0x49, 0x41],  # 45 E
    [0x7F, 0x09, 0x09, 0x09, 0x01],  # 46 F
    [0x3E, 0x41, 0x49, 0x49, 0x7A],  # 47 G
    [0x7F, 0x08, 0x08, 0x08, 0x7F],  # 48 H
    [0x00, 0x41, 0x7F, 0x41, 0x00],  # 49 I
    [0x20, 0x40, 0x41, 0x3F, 0x01],  # 4A J
    [0x7F, 0x08, 0x14, 0x22, 0x41],  # 4B K
    [0x7F, 0x40, 0x40, 0x40, 0x40],  # 4C L
    [0x7F, 0x02, 0x0C, 0x02, 0x7F],  # 4D M
    [0x7F, 0x04, 0x08, 0x10, 0x7F],  # 4E N
    [0x3E, 0x41, 0x41, 0x41, 0x3E],  # 4F O
    [0x7F, 0x09, 0x09, 0x09, 0x06],  # 50 P
    [0x3E, 0x41, 0x51, 0x21, 0x5E],  # 51 Q
    [0x7F, 0x09, 0x19, 0x29, 0x46],  # 52 R
    [0x46, 0x49, 0x49, 0x49, 0x31],  # 53 S
    [0x01, 0x01, 0x7F, 0x01, 0x01],  # 54 T
    [0x3F, 0x40, 0x40, 0x40, 0x3F],  # 55 U
    [0x1F, 0x20, 0x40, 0x20, 0x1F],  # 56 V
    [0x3F, 0x40, 0x38, 0x40, 0x3F],  # 57 W
    [0x63, 0x14, 0x08, 0x14, 0x63],  # 58 X
    [0x07, 0x08, 0x70, 0x08, 0x07],  # 59 Y
    [0x61, 0x51, 0x49, 0x45, 0x43],  # 5A Z
    [0x00, 0x7F, 0x41, 0x41, 0x00],  # 5B [
    [0x02, 0x04, 0x08, 0x10, 0x20],  # 5C Backslash
    [0x00, 0x41, 0x41, 0x7F, 0x00],  # 5D ]
    [0x04, 0x02, 0x01, 0x02, 0x04],  # 5E ^
    [0x40, 0x40, 0x40, 0x40, 0x40],  # 5F _
    [0x00, 0x01, 0x02, 0x04, 0x00],  # 60 `
    [0x20, 0x54, 0x54, 0x54, 0x78],  # 61 a
    [0x7F, 0x48, 0x44, 0x44, 0x38],  # 62 b
    [0x38, 0x44, 0x44, 0x44, 0x20],  # 63 c
    [0x38, 0x44, 0x44, 0x48, 0x7F],  # 64 d
    [0x38, 0x54, 0x54, 0x54, 0x18],  # 65 e
    [0x08, 0x7E, 0x09, 0x01, 0x02],  # 66 f
    [0x0C, 0x52, 0x52, 0x52, 0x3E],  # 67 g
    [0x7F, 0x08, 0x04, 0x04, 0x78],  # 68 h
    [0x00, 0x44, 0x7D, 0x40, 0x00],  # 69 i
    [0x20, 0x40, 0x44, 0x3D, 0x00],  # 6A j
    [0x7F, 0x10, 0x28, 0x44, 0x00],  # 6B k
    [0x00, 0x41, 0x7F, 0x40, 0x00],  # 6C l
    [0x7C, 0x04, 0x18, 0x04, 0x78],  # 6D m
    [0x7C, 0x08, 0x04, 0x04, 0x78],  # 6E n
    [0x38, 0x44, 0x44, 0x44, 0x38],  # 6F o
    [0x7C, 0x14, 0x14, 0x14, 0x08],  # 70 p
    [0x08, 0x14, 0x14, 0x18, 0x7C],  # 71 q
    [0x7C, 0x08, 0x04, 0x04, 0x08],  # 72 r
    [0x48, 0x54, 0x54, 0x54, 0x20],  # 73 s
    [0x04, 0x3F, 0x44, 0x40, 0x20],  # 74 t
    [0x3C, 0x40, 0x40, 0x20, 0x7C],  # 75 u
    [0x1C, 0x20, 0x40, 0x20, 0x1C],  # 76 v
    [0x3C, 0x40, 0x30, 0x40, 0x3C],  # 77 w
    [0x44, 0x28, 0x10, 0x28, 0x44],  # 78 x
    [0x0C, 0x50, 0x50, 0x50, 0x3C],  # 79 y
    [0x44, 0x64, 0x54, 0x4C, 0x44],  # 7A z
    [0x00, 0x08, 0x36, 0x41, 0x00],  # 7B {
    [0x00, 0x00, 0x7F, 0x00, 0x00],  # 7C |
    [0x00, 0x41, 0x36, 0x08, 0x00],  # 7D }
    [0x08, 0x08, 0x2A, 0x1C, 0x08],  # 7E ~
    [0x06, 0x09, 0x09, 0x06, 0x00],  # 7F° symbol
]

class OLED_SSD1306_I2C():
    # Define the degree symbol as a class variable
    DEGREE_SYMBOL = '\x7F'  # Assuming you placed the degree symbol at the position 0x7F in the basic_font array

    def __init__(self, width, height, i2c, addr=0x3C, rst=None):
        self.i2c = i2c
        self.addr = addr
        self.rst = rst

        self.buffer = bytearray(width * height // 8)

        if self.rst:
            self.rst_pin = Pin(self.rst, Pin.OUT)
            self.rst_pin.value(1)
            time.sleep_ms(1)
            self.rst_pin.value(0)
            time.sleep_ms(10)
            self.rst_pin.value(1)

        self.WIDTH = width
        self.HEIGHT = height
        self._width = self.WIDTH
        self._height = self.HEIGHT
        self.rotation = 0
        self.cursor_x = 0
        self.cursor_y = 0
        self.textsize_x = 1
        self.textsize_y = 1
        self.textcolor = 0xFFFF
        self.textbgcolor = 0xFFFF
        self.wrap = True
        self._cp437 = False
        self.gfx_font = None

        self.init_display()

    def init_display(self):
        self.write_cmd(0xAE)  # Display off
        self.write_cmd(0x20)  # Set Memory Addressing Mode
        self.write_cmd(0x10)  # Page Addressing Mode
        self.write_cmd(0xB0)  # Set Page Start Address for Page Addressing Mode, 0-7
        self.write_cmd(0xC8)  # Set COM Output Scan Direction (remapped mode)
        self.write_cmd(0x00)  # ---set low column address
        self.write_cmd(0x10)  # ---set high column address
        self.write_cmd(0x40)  # --set start line address
        self.write_cmd(0x81)  # Set contrast control register
        self.write_cmd(0xFF)
        self.write_cmd(0xA1)  # Set Segment Re-map
        self.write_cmd(0xA6)  # Set display mode. A6=Normal; A7=Inverse

        # Adjust settings based on the display height
        if self.HEIGHT == 64:
            self.write_cmd(0xA8)  # Set multiplex ratio
            self.write_cmd(0x3F)  # 1/64 duty (0x3F)
            self.write_cmd(0xD3)  # Set display offset
            self.write_cmd(0x00)  # No offset
            self.write_cmd(0xDA)  # Set COM pins hardware configuration
            self.write_cmd(0x12)  # Alternative COM pin configuration, disable COM Left/Right remap
        elif self.HEIGHT == 32:
            self.write_cmd(0xA8)  # Set multiplex ratio
            self.write_cmd(0x1F)  # 1/32 duty (0x1F)
            self.write_cmd(0xD3)  # Set display offset
            self.write_cmd(0x00)  # No offset
            self.write_cmd(0xDA)  # Set COM pins hardware configuration
            self.write_cmd(0x02)  # Sequential COM pin configuration, disable COM Left/Right remap
        else:
            raise ValueError("Unsupported display height: {}".format(self.HEIGHT))

        self.write_cmd(0xD5)  # Set display clock divide ratio/oscillator frequency
        self.write_cmd(0x80)  # Suggested value 0x80
        self.write_cmd(0xD9)  # Set pre-charge period
        self.write_cmd(0xF1)  # Suggested value 0xF1
        self.write_cmd(0xDB)  # Set VCOMH deselect level
        self.write_cmd(0x30)  # Suggested value 0x30
        self.write_cmd(0x8D)  # Charge pump setting
        self.write_cmd(0x14)  # Enable charge pump
        self.write_cmd(0xAF)  # Turn on SSD1306 panel

    def get_char_bitmap(self, char):
        """Returns the bitmap for the specified character."""
        if isinstance(char, str):
            char_code = ord(char)  # Convert character to ASCII
        elif isinstance(char, int):
            char_code = char  # Assume char is already an ASCII code
        else:
            raise TypeError("Unsupported character type")

        if 0x20 <= char_code <= 0x7F:
            return basic_font[char_code - 0x20]
        else:
            return [0x00, 0x00, 0x00, 0x00, 0x00]  # Return a blank space for unsupported characters

    def write_line(self, x0, y0, x1, y1, color):
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = x1 - x0
        dy = abs(y1 - y0)
        err = dx // 2
        ystep = 1 if y0 < y1 else -1

        while x0 <= x1:
            if steep:
                self.write_pixel(y0, x0, color)
            else:
                self.write_pixel(x0, y0, color)
            err -= dy
            if err < 0:
                y0 += ystep
                err += dx
            x0 += 1

    def start_write(self):
        pass

    def write_pixel(self, x, y, color):
        self.draw_pixel(x, y, color)

    def write_fast_vline(self, x, y, h, color):
        self.draw_fast_vline(x, y, h, color)

    def write_fast_hline(self, x, y, w, color):
        self.draw_fast_hline(x, y, w, color)

    def write_fill_rect(self, x, y, w, h, color):
        self.fill_rect(x, y, w, h, color)

    def end_write(self):
        pass

    def draw_fast_vline(self, x, y, h, color):
        self.start_write()
        self.write_line(x, y, x, y + h - 1, color)
        self.end_write()

    def draw_fast_hline(self, x, y, w, color):
        self.start_write()
        self.write_line(x, y, x + w - 1, y, color)
        self.end_write()

    def fill_rect(self, x, y, w, h, color):
        self.start_write()
        for i in range(x, x + w):
            self.write_fast_vline(i, y, h, color)
        self.end_write()

    def fill_screen(self, color):
        self.fill_rect(0, 0, self._width, self._height, color)

    def draw_line(self, x0, y0, x1, y1, color):
        if x0 == x1:
            if y0 > y1:
                y0, y1 = y1, y0
            self.draw_fast_vline(x0, y0, y1 - y0 + 1, color)
        elif y0 == y1:
            if x0 > x1:
                x0, x1 = x1, x0
            self.draw_fast_hline(x0, y0, x1 - x0 + 1, color)
        else:
            self.start_write()
            self.write_line(x0, y0, x1, y1, color)
            self.end_write()

    def draw_circle(self, x0, y0, r, color):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r

        self.start_write()
        self.write_pixel(x0, y0 + r, color)
        self.write_pixel(x0, y0 - r, color)
        self.write_pixel(x0 + r, y0, color)
        self.write_pixel(x0 - r, y0, color)

        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x

            self.write_pixel(x0 + x, y0 + y, color)
            self.write_pixel(x0 - x, y0 + y, color)
            self.write_pixel(x0 + x, y0 - y, color)
            self.write_pixel(x0 - x, y0 - y, color)
            self.write_pixel(x0 + y, y0 + x, color)
            self.write_pixel(x0 - y, y0 + x, color)
            self.write_pixel(x0 + y, y0 - x, color)
            self.write_pixel(x0 - y, y0 - x, color)
        self.end_write()

    def draw_circle_helper(self, x0, y0, r, cornername, color):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r

        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
            if cornername & 0x4:
                self.write_pixel(x0 + x, y0 + y, color)
                self.write_pixel(x0 + y, y0 + x, color)
            if cornername & 0x2:
                self.write_pixel(x0 + x, y0 - y, color)
                self.write_pixel(x0 + y, y0 - x, color)
            if cornername & 0x8:
                self.write_pixel(x0 - y, y0 + x, color)
                self.write_pixel(x0 - x, y0 + y, color)
            if cornername & 0x1:
                self.write_pixel(x0 - y, y0 - x, color)
                self.write_pixel(x0 - x, y0 - y, color)

    def fill_circle(self, x0, y0, r, color):
        self.start_write()
        self.write_fast_vline(x0, y0 - r, 2 * r + 1, color)
        self.fill_circle_helper(x0, y0, r, 3, 0, color)
        self.end_write()

    def fill_circle_helper(self, x0, y0, r, corners, delta, color):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r
        px = x
        py = y

        delta += 1  # Avoid some +1's in the loop

        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
            if x < (y + 1):
                if corners & 1:
                    self.write_fast_vline(x0 + x, y0 - y, 2 * y + delta, color)
                if corners & 2:
                    self.write_fast_vline(x0 - x, y0 - y, 2 * y + delta, color)
            if y != py:
                if corners & 1:
                    self.write_fast_vline(x0 + py, y0 - px, 2 * px + delta, color)
                if corners & 2:
                    self.write_fast_vline(x0 - py, y0 - px, 2 * px + delta, color)
                py = y
            px = x

    def draw_rect(self, x, y, w, h, color):
        self.start_write()
        self.write_fast_hline(x, y, w, color)
        self.write_fast_hline(x, y + h - 1, w, color)
        self.write_fast_vline(x, y, h, color)
        self.write_fast_vline(x + w - 1, y, h, color)
        self.end_write()

    def draw_round_rect(self, x, y, w, h, r, color):
        max_radius = min(w, h) // 2  # 1/2 minor axis
        if r > max_radius:
            r = max_radius
        self.start_write()
        self.write_fast_hline(x + r, y, w - 2 * r, color)         # Top
        self.write_fast_hline(x + r, y + h - 1, w - 2 * r, color) # Bottom
        self.write_fast_vline(x, y + r, h - 2 * r, color)         # Left
        self.write_fast_vline(x + w - 1, y + r, h - 2 * r, color) # Right
        # Draw four corners
        self.draw_circle_helper(x + r, y + r, r, 1, color)
        self.draw_circle_helper(x + w - r - 1, y + r, r, 2, color)
        self.draw_circle_helper(x + w - r - 1, y + h - r - 1, r, 4, color)
        self.draw_circle_helper(x + r, y + h - r - 1, r, 8, color)
        self.end_write()

    def fill_round_rect(self, x, y, w, h, r, color):
        max_radius = min(w, h) // 2  # 1/2 minor axis
        if r > max_radius:
            r = max_radius
        self.start_write()
        self.write_fill_rect(x + r, y, w - 2 * r, h, color)
        # Draw four corners
        self.fill_circle_helper(x + w - r - 1, y + r, r, 1, h - 2 * r - 1, color)
        self.fill_circle_helper(x + r, y + r, r, 2, h - 2 * r - 1, color)
        self.end_write()

    def draw_triangle(self, x0, y0, x1, y1, x2, y2, color):
        self.draw_line(x0, y0, x1, y1, color)
        self.draw_line(x1, y1, x2, y2, color)
        self.draw_line(x2, y2, x0, y0, color)

    def fill_triangle(self, x0, y0, x1, y1, x2, y2, color):
        if y0 > y1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        if y1 > y2:
            x2, x1 = x1, x2
            y2, y1 = y1, y2
        if y0 > y1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        self.start_write()
        if y0 == y2:  # Handle awkward all-on-same-line case as its own thing
            a = b = x0
            if x1 < a:
                a = x1
            elif x1 > b:
                b = x1
            if x2 < a:
                a = x2
            elif x2 > b:
                b = x2
            self.write_fast_hline(a, y0, b - a + 1, color)
            self.end_write()
            return

        dx01 = x1 - x0
        dy01 = y1 - y0
        dx02 = x2 - x0
        dy02 = y2 - y0
        dx12 = x2 - x1
        dy12 = y2 - y1
        sa = 0
        sb = 0

        if y1 == y2:
            last = y1  # Include y1 scanline
        else:
            last = y1 - 1  # Skip it

        for y in range(y0, last + 1):
            a = x0 + (sa // dy01 if dy01 != 0 else 0)  # Check for zero denominator
            b = x0 + (sb // dy02 if dy02 != 0 else 0)  # Check for zero denominator
            sa += dx01
            sb += dx02
            if a > b:
                a, b = b, a
            self.write_fast_hline(a, y, b - a + 1, color)

        sa = dx12 * (y - y1)
        sb = dx02 * (y - y0)
        for y in range(y, y2 + 1):
            a = x1 + (sa // dy12 if dy12 != 0 else 0)  # Check for zero denominator
            b = x0 + (sb // dy02 if dy02 != 0 else 0)  # Check for zero denominator
            sa += dx12
            sb += dx02
            if a > b:
                a, b = b, a
            self.write_fast_hline(a, y, b - a + 1, color)
        self.end_write()

    def draw_bitmap(self, x, y, bitmap, w, h, color):
        byte_width = (w + 7) // 8
        b = 0

        self.start_write()
        for j in range(h):
            for i in range(w):
                if i & 7:
                    b <<= 1
                else:
                    b = bitmap[j * byte_width + i // 8]
                if b & 0x80:
                    self.write_pixel(x + i, y + j, color)
        self.end_write()

    def draw_bitmap_bg(self, x, y, bitmap, w, h, color, bg):
        byte_width = (w + 7) // 8
        b = 0

        self.start_write()
        for j in range(h):
            for i in range(w):
                if i & 7:
                    b <<= 1
                else:
                    b = bitmap[j * byte_width + i // 8]
                self.write_pixel(x + i, y + j, color if b & 0x80 else bg)
        self.end_write()

    def set_cursor(self, x, y):
        """
        Set the cursor position for text output.

        :param x: The x-coordinate (column) in pixels.
        :param y: The y-coordinate (row) in pixels.
        """
        self.cursor_x = x
        self.cursor_y = y

    def set_text_size(self, size_x, size_y=None):
        if size_y is None:
            size_y = size_x
        self.textsize_x = max(size_x, 1)
        self.textsize_y = max(size_y, 1)

    def set_rotation(self, x):
        self.rotation = x & 3
        if self.rotation == 0 or self.rotation == 2:
            self._width = self.WIDTH
            self._height = self.HEIGHT
        else:
            self._width = self.HEIGHT
            self._height = self.WIDTH

    def set_font(self, font):
        if font:
            if not self.gfx_font:
                self.cursor_y += 6
        elif self.gfx_font:
            self.cursor_y -= 6
        self.gfx_font = font

    def get_text_bounds(self, text, x, y):
        min_x, min_y = x, y
        max_x, max_y = x, y
        cursor_x, cursor_y = x, y

        for char in text:
            if char == '\n':  # Newline
                cursor_x = x
                cursor_y += self.textsize_y * 8
            elif char != '\r':  # Not a carriage return
                if self.wrap and (cursor_x + self.textsize_x * 6 > self.WIDTH):
                    cursor_x = x
                    cursor_y += self.textsize_y * 8

                x2 = cursor_x + self.textsize_x * 6 - 1
                y2 = cursor_y + self.textsize_y * 8 - 1

                min_x = min(min_x, cursor_x)
                min_y = min(min_y, cursor_y)
                max_x = max(max_x, x2)
                max_y = max(max_y, y2)

                cursor_x += self.textsize_x * 6

        width = max_x - min_x + 1
        height = max_y - min_y + 1

        return min_x, min_y, width, height

    def invert_display(self, invert):
        if invert:
            self.write_cmd(0xA7)  # Inverted display
        else:
            self.write_cmd(0xA6)  # Normal display

    def write_cmd(self, cmd):
        self.i2c.writeto_mem(self.addr, 0x00, bytearray([cmd]))

    def write_data(self, buf):
        self.i2c.writeto_mem(self.addr, 0x40, buf)

    def display(self):
        self.write_cmd(0x21)  # Set column address
        self.write_cmd(0)     # Column start address (0 = reset)
        self.write_cmd(self._width - 1)  # Column end address (127 = reset)
        self.write_cmd(0x22)  # Set page address
        self.write_cmd(0)     # Page start address (0 = reset)
        self.write_cmd((self._height // 8) - 1)  # Page end address
        
        self.write_data(self.buffer)

    def clear_display(self):
        self.buffer = bytearray(self._width * self._height // 8)

    def draw_pixel(self, x, y, color):
        if (x < 0 or x >= self._width or y < 0 or y >= self._height):
            return

        page = y // 8
        shift = y % 8

        if color:
            self.buffer[x + page * self._width] |= (1 << shift)
        else:
            self.buffer[x + page * self._width] &= ~(1 << shift)

    def _write_char(self, char):
        """Write a single character to the display at the current cursor position."""
        if char == '\n':
            self.cursor_x = 0
            self.cursor_y += self.textsize_y * 8
        elif char != '\r':  # Ignore carriage returns
            if self.wrap and ((self.cursor_x + self.textsize_x * 6) > self._width):
                self.cursor_x = 0
                self.cursor_y += self.textsize_y * 8
            self.draw_char(self.cursor_x, self.cursor_y, ord(char), self.textcolor, self.textbgcolor, self.textsize_x, self.textsize_y)
            self.cursor_x += self.textsize_x * 6  # Advance x one char

    def write(self, text):
        if isinstance(text, str):
            for char in text:
                self._write_char(char)
        elif isinstance(text, int):
            self._write_char(chr(text))
        else:
            raise TypeError("Unsupported type for write(): {}".format(type(text)))

    def print(self, text):
        self.write(text)

    def println(self, text):
        self.write(text)
        self.write('\n')

    def draw_char(self, x, y, c, color, bg, size_x, size_y):
        """Draw a character on the display."""
        bitmap = self.get_char_bitmap(c)
        for i in range(5):  # 5 columns per character
            line = bitmap[i]
            for j in range(8):  # 8 rows per character
                if line & 0x1:
                    self.fill_rect(x + i * size_x, y + j * size_y, size_x, size_y, color)
                elif bg != color:
                    self.fill_rect(x + i * size_x, y + j * size_y, size_x, size_y, bg)
                line >>= 1
        if bg != color:  # Fill the background for the 6th column
            self.fill_rect(x + 5 * size_x, y, size_x, 8 * size_y, bg)

