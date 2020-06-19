"""ILI9341 demo (shapes)."""
from time import sleep
from ili9341 import Display, color565
from machine import Pin, SPI


def test():
    """Test code."""
    # Baud rate of 40000000 seems about the max
    spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
    display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17))

    display.clear(color565(64, 0, 255))
    sleep(1)

    display.clear()

    display.draw_hline(10, 319, 229, color565(255, 0, 255))
    sleep(1)

    display.draw_vline(10, 0, 319, color565(0, 255, 255))
    sleep(1)

    display.fill_hrect(23, 50, 30, 75, color565(255, 255, 255))
    sleep(1)

    display.draw_hline(0, 0, 222, color565(255, 0, 0))
    sleep(1)

    display.draw_line(127, 0, 64, 127, color565(255, 255, 0))
    sleep(2)

    display.clear()

    coords = [[0, 63], [78, 80], [122, 92], [50, 50], [78, 15], [0, 63]]
    display.draw_lines(coords, color565(0, 255, 255))
    sleep(1)

    display.clear()
    display.fill_polygon(7, 120, 120, 100, color565(0, 255, 0))
    sleep(1)

    display.fill_rectangle(0, 0, 15, 227, color565(255, 0, 0))
    sleep(1)

    display.clear()

    display.fill_rectangle(0, 0, 163, 163, color565(128, 128, 255))
    sleep(1)

    display.draw_rectangle(0, 64, 163, 163, color565(255, 0, 255))
    sleep(1)

    display.fill_rectangle(64, 0, 163, 163, color565(128, 0, 255))
    sleep(1)

    display.draw_polygon(3, 120, 286, 30, color565(0, 64, 255), rotate=15)
    sleep(3)

    display.clear()

    display.fill_circle(132, 132, 70, color565(0, 255, 0))
    sleep(1)

    display.draw_circle(132, 96, 70, color565(0, 0, 255))
    sleep(1)

    display.fill_ellipse(96, 96, 30, 16, color565(255, 0, 0))
    sleep(1)

    display.draw_ellipse(96, 256, 16, 30, color565(255, 255, 0))

    sleep(5)
    display.cleanup()


test()
