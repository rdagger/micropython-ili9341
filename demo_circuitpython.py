"""ILI9341 demo (CircuitPython Text, Shape & Sprite)."""
import board
from busio import SPI
from digitalio import DigitalInOut
from ili9341 import Display, color565
from xglcd_font import XglcdFont
from time import monotonic, sleep
from sys import exit, implementation


class BouncingSprite(object):
    """Bouncing Sprite."""

    def __init__(self, path, w, h, screen_width, screen_height,
                 speed, display):
        """Initialize sprite.

        Args:
            path (string): Path of sprite image.
            w, h (int): Width and height of image.
            screen_width (int): Width of screen.
            screen_height (int): Width of height.
            size (int): Square side length.
            speed(int): Initial XY-Speed of sprite.
            display (ILI9341): display object.
            color (int): RGB565 color value.
        """
        self.buf = display.load_sprite(path, w, h)
        self.w = w
        self.h = h
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.display = display
        self.x_speed = speed
        self.y_speed = speed
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2
        self.prev_x = self.x
        self.prev_y = self.y

    def update_pos(self):
        """Update sprite speed and position."""
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        x_speed = abs(self.x_speed)
        y_speed = abs(self.y_speed)

        if x + w + x_speed >= self.screen_width:
            self.x_speed = -x_speed
        elif x - x_speed < 0:
            self.x_speed = x_speed

        if y + h + y_speed >= self.screen_height:
            self.y_speed = -y_speed
        elif y - y_speed <= 20:
            self.y_speed = y_speed

        self.prev_x = x
        self.prev_y = y

        self.x = x + self.x_speed
        self.y = y + self.y_speed

    def draw(self):
        """Draw sprite."""
        x = self.x
        y = self.y
        prev_x = self.prev_x
        prev_y = self.prev_y
        w = self.w
        h = self.h
        x_speed = abs(self.x_speed)
        y_speed = abs(self.y_speed)

        # Determine direction and remove previous portion of sprite
        if prev_x > x:
            # Left
            self.display.fill_vrect(x + w, prev_y, x_speed, h, 0)
        elif prev_x < x:
            # Right
            self.display.fill_vrect(x - x_speed, prev_y, x_speed, h, 0)
        if prev_y > y:
            # Upward
            self.display.fill_vrect(prev_x, y + h, w, y_speed, 0)
        elif prev_y < y:
            # Downward
            self.display.fill_vrect(prev_x, y - y_speed, w, y_speed, 0)

        self.display.draw_sprite(self.buf, x, y, w, h)


def test():
    """CircuitPython Text, Shape & Sprite"""
    if implementation.name != 'circuitpython':
        print()
        print('This demo is for CircuitPython only!')
        exit()
    try:
        # Configuratoin for CS and DC pins:
        cs_pin = DigitalInOut(board.P0_15)
        dc_pin = DigitalInOut(board.P0_17)
        rst_pin = DigitalInOut(board.P0_20)

        # Setup SPI bus using hardware SPI:
        spi = SPI(clock=board.P0_24, MOSI=board.P0_22)

        # Create the ILI9341 display:
        display = Display(spi, dc=dc_pin, cs=cs_pin, rst=rst_pin)
        display.clear()

        # Load Fixed Font
        fixed = XglcdFont('fonts/FixedFont5x8.c', 5, 8, letter_count=96)

        # Title
        WIDTH = 128
        text = 'CircuitPython Demo'
        # Measure text and center
        length = fixed.measure_text(text)
        x = int((WIDTH / 2) - (length / 2))
        display.draw_text(x, 6, text, fixed, color565(255, 255, 0))

        # Draw title outline
        display.draw_rectangle(0, 0, 127, 20, color565(0, 255, 0))

        # Load sprite
        logo = BouncingSprite('images/blinka45x48.raw',
                              45, 48, 239, 319, 1, display)

        while True:
            timer = monotonic()
            logo.update_pos()
            logo.draw()
            # Attempt to set framerate to 30 FPS
            timer_dif = .033333333 - (monotonic() - timer)
            if timer_dif > 0:
                sleep(timer_dif)

    except KeyboardInterrupt:
        display.cleanup()


test()
