"""ILI9341 demo (color wheel)."""
from time import sleep
from ili9341 import Display, color565
from machine import Pin, SPI  # type: ignore
from math import cos, pi, sin

ANGLE_STEP_SIZE = 0.05  # Decrease step size for higher resolution
PI2 = pi * 2


def hsv_to_rgb(h, s, v):
    """
    Convert HSV to RGB (based on colorsys.py).

        Args:
            h (float): Hue 0 to 1.
            s (float): Saturation 0 to 1.
            v (float): Value 0 to 1 (Brightness).
    """
    if s == 0.0:
        return v, v, v
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6

    v = int(v * 255)
    t = int(t * 255)
    p = int(p * 255)
    q = int(q * 255)

    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q


def test():
    """Test code."""
    # Baud rate of 40000000 seems about the max
    spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
    display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17))

    half_width = display.width // 2
    half_height = display.height // 2
    center_x = half_width - 1
    center_y = half_height - 1

    x, y = 0, 0
    angle = 0.0
    #  Loop all angles from 0 to 2 * PI radians
    while angle < PI2:
        # Calculate x, y from a vector with known length and angle
        x = int(center_x * sin(angle) + half_width)
        y = int(center_y * cos(angle) + half_height)
        color = color565(*hsv_to_rgb(angle / PI2, 1, 1))
        display.draw_line(x, y, center_x, center_y, color)
        angle += ANGLE_STEP_SIZE

    sleep(5)

    for r in range(center_x, 0, -1):
        color = color565(*hsv_to_rgb(r / half_width, 1, 1))
        display.fill_circle(center_x, center_y, r, color)

    sleep(9)
    display.cleanup()


test()
