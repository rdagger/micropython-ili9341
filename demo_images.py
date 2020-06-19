"""ILI9341 demo (images)."""
from time import sleep
from ili9341 import Display
from machine import Pin, SPI


def test():
    """Test code."""
    # Baud rate of 40000000 seems about the max
    spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
    display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17))

    display.draw_image('images/RaspberryPiWB128x128.raw', 0, 0, 128, 128)
    sleep(2)

    display.draw_image('images/MicroPython128x128.raw', 0, 129, 128, 128)
    sleep(2)

    display.draw_image('images/Tabby128x128.raw', 112, 0, 128, 128)
    sleep(2)

    display.draw_image('images/Tortie128x128.raw', 112, 129, 128, 128)

    sleep(9)

    display.cleanup()


test()
