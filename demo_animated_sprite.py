"""ILI9341 demo (animated sprite).

    Note:  This demo requires a board with additional PSRAM.
"""
from ili9341 import Display
from machine import Pin, SPI  # type: ignore
from micropython import const  # type: ignore
from utime import sleep_us, ticks_us, ticks_diff  # type: ignore

SPRITE_WIDTH = const(221)
SPRITE_HEIGHT = const(154)
SPRITE_COUNT = const(8)
SIZE = const(68068)  # width (221) x height (154) x bytes of color (2)


def test():
    """Animated sprite."""
    try:
        # Baud rate of 40000000 seems about the max
        spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
        display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17))
        display.clear()

        # Load sprite
        cat = display.load_sprite('images/Cat221x1232.raw',
                                  SPRITE_WIDTH, SPRITE_HEIGHT * SPRITE_COUNT)
        # Use memoryview to improve memory usage
        mv_cat = memoryview(cat)

        x = (display.width - SPRITE_WIDTH) // 2
        y = (display.height - SPRITE_HEIGHT) // 2
        index = 0  # Sprite frame index

        while True:
            timer = ticks_us()
            offset = SIZE * index
            display.draw_sprite(mv_cat[offset: offset + SIZE], x, y,
                                SPRITE_WIDTH, SPRITE_HEIGHT)
            index += 1  # Increment sprite index
            index &= 7  # Wrap sprite index on end sprite

            # Attempt to set framerate to 30 FPS
            timer_dif = 33333 - ticks_diff(ticks_us(), timer)
            if timer_dif > 0:
                sleep_us(timer_dif)

    except KeyboardInterrupt:
        display.cleanup()


test()
