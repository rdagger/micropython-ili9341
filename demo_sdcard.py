"""ILI9341 demo (SD Card with touchscreen demo).

The Micropython Machine SDCard library can cause conflicts with the ILI9341.
Therefore, I'm using micropython-lib sdcard.py to control the SD Card.
https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/storage/sdcard

The SD Card should be set to the same SPI bus as the touchscreen because they
both run at slower speeds.  The display should be run on its own SPI bus to
take advantage of the higher bandwidth.

If your board has a built-in SD card then you will want to identify what GPIO
pins and what SPI bus it uses.  This demo was tested using a Lolin 32 Pro
which uses bus 1 (HSPI) for the SD card and GPIO pin 13 for CS.  Therefore,
the SD Card and the touch screen will share HSPI and the display will be on
VSPI.

Demo requires the Python41x49.raw image to be copied to the  SD card.  The
SD card should be formatted to Fat32.
"""
from ili9341 import Display, color565
from xpt2046 import Touch
from machine import idle, Pin, SPI  # type: ignore
from sdcard import SDCard
import os


class Demo(object):
    """SD Card with touchscreen demo."""
    CYAN = color565(0, 255, 255)
    PURPLE = color565(255, 0, 255)
    WHITE = color565(255, 255, 255)

    def __init__(self, display, spi2):
        """Initialize box.

        Args:
            display (ILI9341): display object
            spi2 (SPI): SPI bus
        Notes:
            Some ILI9341's require touchscreen width & height to be swapped
            when the Touch class is initialized.
        """
        self.display = display
        self.touch = Touch(spi2, cs=Pin(5), int_pin=Pin(0),
                           int_handler=self.touchscreen_press,
                           width=240, height=320)
        # Display initial message
        self.display.draw_text8x8(self.display.width // 2 - 32,
                                  self.display.height - 9,
                                  "TOUCH ME",
                                  self.WHITE,
                                  background=self.PURPLE)

    def touchscreen_press(self, x, y):
        """Process touchscreen press events."""
        # x, y = y, x  # Some screens require swapping X and Y
        # x = (self.display.width - 1) - x  # Some screens require flipping X
        y = (self.display.height - 1) - y  # Some screens require flipping Y

        # Display coordinates
        self.display.draw_text8x8(self.display.width // 2 - 32,
                                  self.display.height - 9,
                                  "{0:03d}, {1:03d}".format(x, y),
                                  self.CYAN)

        # Draw image from SD Card
        try:
            x -= 20  # Image center X
            y -= 25  # Image center Y
            x = max(x, 41)
            x = min(x, self.display.width - 42)
            y = max(y, 49)
            y = min(y, self.display.height - 50)
            self.display.draw_image('sd/Python41x49.raw', x, y, 41, 49)
        except OSError as e:
            print("Error:", e)


def test():
    """Test code."""
    # Initialize SPI bus for touch screen & built-in SD card (bus must match).
    spi1 = SPI(1, baudrate=1000000, sck=Pin(14), mosi=Pin(15), miso=Pin(2))
    # Initialize and mount SD card
    sd_cs = Pin(13)  # When using an internal SD card, ensure CS matches.
    sd = SDCard(spi1, sd_cs)
    os.mount(sd, '/sd')
    # Initialize SPI bus for display
    spi2 = SPI(2, baudrate=40000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
    display = Display(spi2, dc=Pin(22), cs=Pin(19), rst=Pin(21))

    Demo(display, spi1)

    try:
        while True:
            idle()

    except KeyboardInterrupt:
        print("\nCtrl-C pressed.  Cleaning up and exiting...")
    finally:
        display.cleanup()  # Clean up display
        os.umount('/sd')  # Unmount SD card


test()
