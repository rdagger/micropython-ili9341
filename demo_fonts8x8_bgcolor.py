"""ILI9341 demo (fonts 8x8 background color)."""
from time import sleep
from ili9341 import Display, color565
from machine import Pin, SPI  # type: ignore


def test():
    """Test code."""
    spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
    display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17))

    display.draw_text8x8(0, 0, 'Built-in', color565(255, 0, 0))
    display.fill_rectangle(0, 10, 104, 12, color565(255, 0, 0))
    display.draw_text8x8(0, 12, 'Built-in', color565(0, 0, 0),
                         color565(255, 0, 0))

    display.draw_text8x8(0, 30, 'MicroPython', color565(0, 255, 0))
    display.fill_rectangle(0, 40, 104, 12, color565(0, 255, 0))
    display.draw_text8x8(0, 42, 'MicroPython', color565(0, 0, 0),
                         color565(0, 255, 0))

    display.draw_text8x8(0, 60, '8x8 Font', color565(0, 0, 255))
    display.fill_rectangle(0, 70, 104, 12, color565(0, 0, 255))
    display.draw_text8x8(0, 72, '8x8 Font', color565(0, 0, 0),
                         color565(0, 0, 255))

    display.draw_text8x8(0, 90, 'No Background', color565(255, 255, 255))
    display.fill_rectangle(0, 100, 104, 12, color565(255, 255, 255))
    display.draw_text8x8(0, 102, 'No Background', color565(255, 255, 255))

    y_center = display.height // 2
    display.draw_text8x8(display.width - 10, y_center - 48, "Rotate = 270",
                         color565(0, 255, 255), color565(255, 0, 255),
                         rotate=270)

    sleep(15)
    display.cleanup()


test()
