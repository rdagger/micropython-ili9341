"""XPT2046 Touch module."""
import time


class Touch(object):
    """Serial interface for XPT2046 Touch Screen Controller."""

    # Command constants from ILI9341 datasheet
    GET_X = const(0b11010000)  # X position
    GET_Y = const(0b10010000)  # Y position
    GET_Z1 = const(0b10110000)  # Z1 position
    GET_Z2 = const(0b11000000)  # Z2 position
    GET_TEMP0 = const(0b10000000)  # Temperature 0
    GET_TEMP1 = const(0b11110000)  # Temperature 1
    GET_BATTERY = const(0b10100000)  # Battery monitor
    GET_AUX = const(0b11100000)  # Auxiliary input to ADC

    def __init__(self, spi, cs, int_pin=None, int_handler=None,
                 width=240, height=320,
                 x_min=100, x_max=1962, y_min=100, y_max=1900, rotation=0):
        """Initialize touch screen controller.

        Args:
            spi (Class Spi):  SPI interface for OLED
            cs (Class Pin):  Chip select pin
            int_pin (Class Pin):  Touch controller interrupt pin
            int_handler (function): Handler for screen interrupt
            width (int): Width of LCD screen
            height (int): Height of LCD screen
            x_min (int): Minimum x coordinate
            x_max (int): Maximum x coordinate
            y_min (int): Minimum Y coordinate
            y_max (int): Maximum Y coordinate
        """
        self.spi = spi
        self.cs = cs
        self.cs.init(self.cs.OUT, value=1)
        self.rx_buf = bytearray(3)  # Receive buffer
        self.tx_buf = bytearray(3)  # Transmit buffer
        self.width = width
        self.height = height
        # Set calibration
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.rotation = rotation
        self.last_touch=0
        self.x_multiplier = width / (x_max - x_min)
        self.x_add = x_min * -self.x_multiplier
        self.y_multiplier = height / (y_max - y_min)
        self.y_add = y_min * -self.y_multiplier

        if int_pin is not None:
            self.int_pin = int_pin
            self.int_pin.init(int_pin.IN)
            self.int_handler = int_handler
            self.int_locked = False
            int_pin.irq(trigger=int_pin.IRQ_FALLING | int_pin.IRQ_RISING,
                        handler=self.int_press)


    def rot(self,x,y,rotation=None): # convert touch locations to possibly-rotated screen locations.
        if rotation is None:
            rotation=self.rotation

        x,y = self.normalize(x,y)

        if rotation == 0:
            return x, self.height - y - 1
        elif rotation == 90:
            return self.height - y - 1, self.width - x - 1
        elif rotation == 180:
            return self.width - x - 1, y
        elif rotation == 270:
            return y , x


    def get_touch(self):
        """Take multiple samples to get accurate touch reading."""
        timeout = 2  # set timeout to 2 seconds
        confidence = 5
        buff = [[0, 0] for x in range(confidence)]
        buf_length = confidence  # Require a confidence of 5 good samples
        buffptr = 0  # Track current buffer position
        nsamples = 0  # Count samples
        while timeout > 0:
            if nsamples == buf_length:
                meanx = sum([c[0] for c in buff]) // buf_length
                meany = sum([c[1] for c in buff]) // buf_length
                dev = sum([(c[0] - meanx)**2 +
                          (c[1] - meany)**2 for c in buff]) / buf_length
                if dev <= 50:  # Deviation should be under margin of 50
                    return self.normalize(meanx, meany)
            # get a new value
            sample = self.raw_touch(True)  # get a touch
            if sample is None:
                nsamples = 0    # Invalidate buff
            else:
                buff[buffptr] = sample  # put in buff
                buffptr = (buffptr + 1) % buf_length  # Incr, until rollover
                nsamples = min(nsamples + 1, buf_length)  # Incr. until max

            time.sleep(.05)
            timeout -= .05
        return None

    def int_press(self, pin):
        """Send X,Y values to passed interrupt handler."""
        if not pin.value() and not self.int_locked:
            self.int_locked = True  # Lock Interrupt
            buff = self.raw_touch(True)

            if buff is not None:
                x, y = self.normalize(*buff)
                self.int_handler(x, y)
            time.sleep(.1)  # Debounce falling edge
        elif pin.value() and self.int_locked:
            time.sleep(.1)  # Debounce rising edge
            self.int_locked = False  # Unlock interrupt

    def normalize(self, x, y):
        """Normalize mean X,Y values to match LCD screen."""
        x = int(self.x_multiplier * x + self.x_add)
        y = int(self.y_multiplier * y + self.y_add)
        return x, y

    def raw_touch(self,xyonly=False,nozero=True):
        """Read raw X,Y touch values.

        Returns:
            tuple(int, int): X, Y
        """
        x = self.send_command(self.GET_X)
        y = self.send_command(self.GET_Y)
        if xyonly:
            if self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max:
                return (x, y)
            else:
                return None
        else: # some boards give spurious touch events, which can be filtered out by looking at pressure and timing
            z1 = self.send_command(self.GET_Z1) # pressure
            z2 = self.send_command(self.GET_Z2)
            t0 = self.send_command(self.GET_TEMP0) # temperature
            t1 = self.send_command(self.GET_TEMP1)
            b = self.send_command(self.GET_BATTERY)
            a = self.send_command(self.GET_AUX) # chip aux ADC input
            p = x * (z1 - z2) / z1 if z1>0 else None # touch-pressure is a formula based on x
            p2 = x/4096 * (z2/z1-1) if z1>0 else None # touch-pressure is a formula based on x
            d = None
            if p is not None:
                now=time.ticks_ms()
                d = time.ticks_diff(now, self.last_touch) # timediff since last (for debounce)
                self.last_touch=now
            return (p, x, y, z1, z2, t0, t1, b, a, d, p2) + tuple(self.normalize(x,y) + tuple(self.rot(x,y))) # cnd

    def send_command(self, command):
        """Write command to XT2046 (MicroPython).

        Args:
            command (byte): XT2046 command code.
        Returns:
            int: 12 bit response
        """
        self.tx_buf[0] = command
        self.cs(0)
        self.spi.write_readinto(self.tx_buf, self.rx_buf)
        self.cs(1)

        return (self.rx_buf[1] << 4) | (self.rx_buf[2] >> 4)



""" Examples

import time
from xpt2046 import Touch
from machine import Pin, SPI, ADC, PWM, SDCard, SoftSPI
sspi = SoftSPI(baudrate=500000, sck=Pin(25), mosi=Pin(32), miso=Pin(39))
touch = Touch(sspi, cs=Pin(33)) # a, int_pin=Pin(36), int_handler=self._touch_handler)
while True:
time.sleep(0.1)
t = touch.raw_touch() # (p, x, y, z1, z2, t0, t1, b, a, d)
if t[-1] is not None:
print(t)

"""
