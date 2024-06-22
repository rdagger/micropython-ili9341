"""ILI9341 demo (mirror)."""
from time import sleep
from ili9341 import Display, color565
from machine import Pin, SPI  # type: ignore

# Define colors
COLOR_RED = color565(255, 0, 0)
COLOR_BLUE = color565(0, 0, 255)
COLOR_GREEN = color565(0, 255, 0)
COLOR_YELLOW = color565(255, 255, 0)
COLOR_PURPLE = color565(128, 0, 128)
COLOR_CYAN = color565(0, 255, 255)
COLOR_MAGENTA = color565(255, 0, 255)
COLOR_ORANGE = color565(255, 165, 0)
COLOR_WHITE = color565(255, 255, 255)
COLOR_LAVENDER = color565(255, 165, 255)

MIRROR_ROTATE = ((False, 0),
                 (False, 90),
                 (False, 180),
                 (False, 270),
                 (True, 0),
                 (True, 90),
                 (True, 180),
                 (True, 270))


def test():
    """Test code."""
    for mirror, rotation in MIRROR_ROTATE:
        # Baud rate of 40000000 seems about the max
        spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
        # Set width & height based on rotation
        if rotation == 0 or rotation == 180:
            width, height = 240, 320
        else:
            width, height = 320, 240
        display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17),
                          width=width, height=height,
                          rotation=rotation, mirror=mirror)
        display.clear()

        # Outer Vertical Line
        display.draw_line(41, 21, 41, 239, COLOR_RED)

        # Inner Vertical Line
        display.draw_line(61, 41, 61, 239, COLOR_BLUE)

        # Outer Top Horizontal Line
        display.draw_line(41, 21, 181, 21, COLOR_GREEN)

        # Inner Top Horizontal Line
        display.draw_line(61, 41, 181, 41, COLOR_YELLOW)

        # Outer Middle Horizontal Line
        display.draw_line(62, 130, 161, 130, COLOR_PURPLE)

        # Inner Middle Horizontal Line
        display.draw_line(62, 111, 161, 111, COLOR_CYAN)

        # End Cap on Outer Vertical Line (Bottom)
        display.draw_line(41, 239, 61, 239, COLOR_MAGENTA)

        # End Cap on Outer Top Horizontal Line (Right)
        display.draw_line(181, 21, 181, 41, COLOR_ORANGE)

        # End Caps on Inner Lines (Middle)
        display.draw_line(162, 111, 162, 130, COLOR_WHITE)

        # Display rotation and mirror values at bottom of display
        text = f"Rotation: {rotation}, Mirror: {mirror}"
        display.draw_text8x8(
            (width - len(text) * 8) // 2 if width < 320 else 90,
            height - 50 if width < 320 else height - 9,
            text,
            COLOR_LAVENDER)

        sleep(5)
        display.cleanup()


test()
