"""ILI9341 demo (inversion)."""
from time import sleep
from ili9341 import Display, color565
from machine import Pin, SPI  # type: ignore


def test():
    """Test code."""
    # Baud rate of 40000000 seems about the max
    spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
    display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17))

    display.clear()
    display.fill_rectangle(0, 0, 100, 100, color565(255, 0, 0))
    display.fill_polygon(3, 140, 140, 70, color565(0, 255, 0), rotate=15)
    display.fill_circle(170, 240, 50, color565(0, 0, 255))

    sleep(2)
    display.invert()

    sleep(5)
    display.invert(False)

    sleep(2)
    display.cleanup()


test()
