"""Search online for pwned passwords."""
from machine import Pin, SPI
from hashlib import sha1
from ubinascii import hexlify
from urequests2 import get
from network import STA_IF, WLAN
import gc
from xpt2046 import Touch
from ili9341 import Display, color565
from xglcd_font import XglcdFont
from touch_keyboard import TouchKeyboard
from time import sleep


class PwnLookup(object):
    """Checks if password is pwned."""

    def __init__(self, spi1, spi2, dc=4, cs1=16, rst=17, cs2=5, rotation=270):
        """Initialize PwnLookup."""
        # Set up display
        self.display = Display(spi1, dc=Pin(dc), cs=Pin(cs1), rst=Pin(rst),
                               width=320, height=240, rotation=rotation)

        # Load font
        self.unispace = XglcdFont('fonts/Unispace12x24.c', 12, 24)

        # Set up Keyboard
        self.keyboard = TouchKeyboard(self.display, self.unispace)

        # Set up touchscreen
        self.xpt = Touch(spi2, cs=Pin(cs2), int_pin=Pin(0),
                         int_handler=self.touchscreen_press)
        self.wlan = WLAN(STA_IF)

    def lookup(self, pwd):
        """Return the number of times password found in pwned database.

        Args:
            pwd: password to check
        Returns:
            integer: password hits from online pwned database.
        Raises:
            IOError: if there was an error due to WiFi network.
            RuntimeError: if there was an error trying to fetch data from dB.
            UnicodeError: if there was an error UTF_encoding the password.
        """
        sha1pwd = sha1(pwd.encode('utf-8')).digest()
        sha1pwd = hexlify(sha1pwd).upper().decode('utf-8')
        head, tail = sha1pwd[:5], sha1pwd[5:]

        if not self.wlan.isconnected():
            raise IOError('WiFi network error')

        hits = 0
        gc.collect()
        with get('https://api.pwnedpasswords.com/range/' + head) as response:
            for line in response.iter_lines():
                l = line.decode(response.encoding).split(":")
                if l[0] == tail:
                    hits = int(l[1])
                    break
        gc.collect()

        return hits

    def touchscreen_press(self, x, y):
        """Process touchscreen press events."""
        if self.keyboard.handle_keypress(x, y, debug=False) is True:
            self.keyboard.locked = True
            pwd = self.keyboard.kb_text

            self.keyboard.show_message("Searching...", color565(0, 0, 255))
            try:
                hits = self.lookup(pwd)

                if hits:
                    # Password found
                    msg = "PASSWORD HITS: {0}".format(hits)
                    self.keyboard.show_message(msg, color565(255, 0, 0))
                else:
                    # Password not found
                    msg = "PASSWORD NOT FOUND"
                    self.keyboard.show_message(msg, color565(0, 255, 0))
            except Exception as e:
                if hasattr(e, 'message'):
                    self.keyboard.show_message(e.message[:22],
                                               color565(255, 255, 255))
                else:
                    self.keyboard.show_message(str(e)[:22],
                                               color565(255, 255, 255))

            self.keyboard.waiting = True
            self.keyboard.locked = False


def main():
    """Start PwnLookup."""
    spi1 = SPI(1, baudrate=51200000,
               sck=Pin(14), mosi=Pin(13), miso=Pin(12))
    spi2 = SPI(2, baudrate=1000000,
               sck=Pin(18), mosi=Pin(23), miso=Pin(19))

    PwnLookup(spi1, spi2)

    while True:
        sleep(.1)


main()
