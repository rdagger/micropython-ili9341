"""ILI9341 demo (fonts 8x8 background color)."""
from time import sleep
from ili9341 import Display, color565
from machine import Pin, SPI  # type: ignore


def test():
    """Test code."""
    spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
    display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17))

    display.draw_text8x8(0, 0, 'Built-in', color565(255, 0, 0))
    display.fill_rectangle(0, 10, 127, 20, color565(255, 0, 0))
    display.draw_text8x8(0, 15, 'Built-in', color565(0, 0, 0),
                         color565(255, 0, 0))

    display.draw_text8x8(0, 40, 'MicroPython', color565(0, 255, 0))
    display.fill_rectangle(0, 50, 127, 20, color565(0, 255, 0))
    display.draw_text8x8(0, 55, 'MicroPython-in', color565(0, 0, 0),
                         color565(0, 255, 0))

    display.draw_text8x8(0, 80, '8x8 Font', color565(0, 0, 255))
    display.fill_rectangle(0, 90, 127, 20, color565(0, 0, 255))
    display.draw_text8x8(0, 95, '8x8 Font', color565(0, 0, 0),
                         color565(0, 0, 255))

    display.draw_text8x8(0, 120, 'Built-in', color565(255, 255, 0))
    display.fill_rectangle(0, 130, 127, 20, color565(255, 255, 0))
    display.draw_text8x8(0, 135, 'Built-in', color565(0, 0, 0),
                         color565(255, 255, 0))

    display.draw_text8x8(0, 160, 'MicroPython', color565(0, 255, 255))
    display.fill_rectangle(0, 170, 127, 20, color565(0, 255, 255))
    display.draw_text8x8(0, 175, 'MicroPython-in', color565(0, 0, 0),
                         color565(0, 255, 255))

    display.draw_text8x8(0, 200, '8x8 Font', color565(255, 0, 255))
    display.fill_rectangle(0, 210, 127, 20, color565(255, 0, 255))
    display.draw_text8x8(0, 215, '8x8 Font', color565(0, 0, 0),
                         color565(255, 0, 255))
    
    display.draw_text8x8(0, 240, 'No Background', color565(255, 255, 255))
    display.fill_rectangle(0, 250, 127, 20, color565(255, 255, 255))
    display.draw_text8x8(0, 255, 'No Background', color565(255, 255, 255))

    y_center = display.height // 2
    display.draw_text8x8(display.width - 29, y_center - 48, "Rotate = 270",
                         color565(255, 255, 255), rotate=270)
    display.fill_rectangle(display.width - 19, 60, 18, 200,
                           color565(255, 128, 0))
    display.draw_text8x8(display.width - 14, y_center - 48, "Rotate = 270",
                         color565(255, 255, 255), rotate=270,
                         background=color565(255, 128, 0))

    sleep(15)
    display.cleanup()


test()
