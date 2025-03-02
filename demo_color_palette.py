"""ILI9341 demo (color palette)."""
from time import sleep
from ili9341 import Display, color565
from machine import Pin, SPI  # type: ignore


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

    radius = 9
    step_size = (radius + 1) * 2
    num_circles_x = (display.width // step_size)
    num_circles_y = (display.height // step_size)
    total_circles = num_circles_x * num_circles_y
    c = 0
    for x in range(0, num_circles_x):
        for y in range(0, num_circles_y):
            color = color565(*hsv_to_rgb(c / total_circles, 1, 1))
            display.fill_circle(x * step_size + radius, y * step_size + radius,
                                radius, color)
            c += 1

    sleep(9)
    display.cleanup()


test()
