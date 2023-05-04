"""ILI9341 demo (clear)."""
from time import sleep, ticks_ms
from ili9341 import Display, color565
from machine import Pin, SPI
import gc

valid_hlines = [1, 2, 4, 5, 8, 10, 16, 20, 32, 40, 64, 80, 160]

colors = {
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "AQUA": (0, 255, 255),
    "MAROON": (128, 0, 0),
    "DARKGREEN": (0, 128, 0),
    "NAVY": (0, 0, 128),
    "TEAL": (0, 128, 128),
    "PURPLE": (128, 0, 128),
    "ORANGE": (255, 128, 0),
    "DEEP_PINK": (255, 0, 128),
    "CYAN": (128, 255, 255),
}

def test():
    """Test code."""
    # Baud rate of 40000000 seems about the max
    spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
    display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17))

    print('Clearing to black...')
    start = ticks_ms()
    display.clear()
    end = ticks_ms()
    print(f'Display cleared in {end - start} ms.')
    sleep(2)

    print('Clearing to white...')
    start = ticks_ms()
    display.clear(color565(255, 255, 255))
    end = ticks_ms()
    print(f'Display cleared in {end - start} ms.')
    sleep(2)

    for hlines, (color, rgb) in zip(valid_hlines, colors.items()):
        gc.collect()
        print(f'Clearing display to {color}, hlines={hlines}...')
        try:
            start = ticks_ms()
            display.clear(hlines=hlines, color=color565(*rgb))
            end = ticks_ms()
            print(f'Display cleared in {end - start} ms.')
        except Exception as e:
            print(e)
        sleep(1)

    sleep(5)
    display.cleanup()


test()
