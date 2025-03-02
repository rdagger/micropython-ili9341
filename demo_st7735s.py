"""ILI9341 demo (ST7735s)."""
from time import sleep
from ili9341 import Display
from xglcd_font import XglcdFont
from machine import Pin, SPI  # type: ignore
from micropython import const  # type: ignore

WHITE = const(0XFFFF)  # (255, 255, 255)
RED = const(0XF800)  # (255, 0, 0)
GREEN = const(0X07E0)  # (0, 255, 0)
BLUE = const(0X001F)  # (0, 0, 255)
INDIGO = const(0X801F)  # (128, 0, 255)


def test():
    """Test code."""
    # Baud rate of 40000000 seems about the max
    # spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
    spi = SPI(1, baudrate=40000000, sck=Pin(12), mosi=Pin(11))
    display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17),
                      width=128, height=160,
                      mirror=True, bgr=False, gamma=True,
                      x_offset=2, y_offset=1)

    robotron = XglcdFont('fonts/Robotron13x21.c', 13, 21)

    display.clear()

    display.draw_rectangle(0, 0, 128, 160, WHITE)

    display.draw_text8x8(0, 0, 'Top-Left', INDIGO)

    display.draw_text(20, 30, 'RED', robotron, RED)
    display.draw_text(20, 70, 'GREEN', robotron, GREEN)
    display.draw_text(20, 110, 'BLUE', robotron, BLUE)

    display.draw_image('images/Python41x49.raw', 86, 110, 41, 49)

    sleep(15)
    display.cleanup()


test()
