"""ILI9341 demo (colored squares)."""
from time import sleep
from ili9341 import Display, color565
from machine import Pin, SPI  # type: ignore


colors = {
    0: color565(255, 0, 0),  # Red
    1: color565(0, 255, 0),  # Green
    2: color565(0, 0, 255),  # Blue
    3: color565(255, 255, 0),  # Yellow
    4: color565(255, 0, 255),  # Fuchsia
    5: color565(0, 255, 255),  # Aqua
    6: color565(128, 0, 0),  # Maroon
    7: color565(0, 128, 0),  # Dark green
    8: color565(0, 0, 128),  # Navy
    9: color565(0, 128, 128),  # Teal
    10: color565(128, 0, 128),  # Purple
    11: color565(128, 128, 0),  # Olive
    12: color565(255, 128, 0),  # Orange
    13: color565(255, 0, 128),  # Deep pink
    14: color565(128, 255, 0),  # Chartreuse
    15: color565(0, 255, 128),  # Spring green
    16: color565(128, 0, 255),  # Indigo
    17: color565(0, 128, 255),  # Dodger blue
    18: color565(128, 255, 255),  # Cyan
    19: color565(255, 128, 255),  # Pink
    20: color565(255, 255, 128),  # Light yellow
    21: color565(255, 128, 128),  # Light coral
    22: color565(128, 255, 128),  # Light green
    23: color565(128, 128, 255),  # Light slate blue
    24: color565(255, 255, 255),  # White
}


def test():
    """Test code."""
    # Baud rate of 40000000 seems about the max
    spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
    display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17))

    cols = 5  # Number of columns
    rows = 5  # Number of rows
    rect_width = display.width // cols  # Width of each rectangle
    rect_height = display.height // rows  # Height of each rectangle
    c = 0  # Color index
    for row in range(rows):  # Loop through rows
        for col in range(cols):  # Loop through columns
            x = col * rect_width  # Calculate X coordinate
            y = row * rect_height  # Calculate Y coordinate
            display.fill_rectangle(x, y, rect_width - 1, rect_height - 1,
                                   colors[c])  # Draw a filled rectangle
            c += 1  # Increment color index

    sleep(10)
    display.cleanup()


test()
