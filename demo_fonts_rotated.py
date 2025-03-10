"""ILI9341 demo (fonts rotated)."""
from time import sleep
from ili9341 import Display, color565
from machine import Pin, SPI  # type: ignore
from xglcd_font import XglcdFont


def test():
    """Test code."""
    # Baud rate of 40000000 seems about the max
    spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
    display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17))

    print('Loading fonts...')
    print('Loading arcadepix')
    arcadepix = XglcdFont('fonts/ArcadePix9x11.c', 9, 11)
    print('loading espressodolce')
    espressodolce = XglcdFont('fonts/EspressoDolce18x24.c', 18, 24)
    print('Loading neato')
    neato = XglcdFont('fonts/Neato5x7.c', 5, 7, letter_count=223)
    print('Loading robotron')
    robotron = XglcdFont('fonts/Robotron13x21.c', 13, 21)
    print('Loading unispace')
    unispace = XglcdFont('fonts/Unispace12x24.c', 12, 24)

    # ArcadePix
    font_height = arcadepix.height
    display.draw_text(0, 0,
                      'Portrait', arcadepix,
                      color565(255, 255, 0),
                      landscape=False, rotate_180=False)
    text_width = arcadepix.measure_text('Landscape')
    display.draw_text(0, display.height - 1,
                      'Landscape', arcadepix,
                      color565(255, 0, 0),
                      landscape=True, rotate_180=False)
    text_width = arcadepix.measure_text('Port. Rot. 180')
    display.draw_text(display.width - text_width - 1,
                      display.height - font_height,
                      'Port. Rot. 180', arcadepix,
                      color565(255, 0, 255),
                      landscape=False, rotate_180=True)
    text_width = arcadepix.measure_text('Land. Rot. 180')
    display.draw_text(display.width - font_height - 1, text_width,
                      'Land. Rot. 180', arcadepix,
                      color565(0, 0, 255),
                      landscape=True, rotate_180=True)
    sleep(5)

    # Espresso Dolce
    display.clear()
    font_height = espressodolce.height
    display.draw_text(0, 0,
                      'PORT.', espressodolce,
                      color565(255, 255, 0),
                      landscape=False, rotate_180=False)
    text_width = espressodolce.measure_text('LAND.')
    display.draw_text(0, display.height - 1,
                      'LAND.', espressodolce,
                      color565(255, 0, 0),
                      landscape=True, rotate_180=False)
    text_width = espressodolce.measure_text('PORT.')
    display.draw_text(display.width - text_width - 1,
                      display.height - font_height,
                      'PORT.', espressodolce,
                      color565(255, 0, 255),
                      landscape=False, rotate_180=True)
    text_width = espressodolce.measure_text('ROT. 180')
    display.draw_text(display.width - text_width - 1,
                      display.height - font_height * 2,
                      'ROT. 180', espressodolce,
                      color565(255, 0, 255),
                      landscape=False, rotate_180=True)
    text_width = espressodolce.measure_text('LAND.')
    display.draw_text(display.width - font_height - 1, text_width,
                      'LAND.', espressodolce,
                      color565(0, 0, 255),
                      landscape=True, rotate_180=True)
    text_width = espressodolce.measure_text('ROT. 180')
    display.draw_text(display.width - font_height * 2 - 1, text_width,
                      'ROT. 180', espressodolce,
                      color565(0, 0, 255),
                      landscape=True, rotate_180=True)
    sleep(5)

    # Neato
    display.clear()
    font_height = neato.height
    display.draw_text(0, 0,
                      'Portrait', neato,
                      color565(255, 255, 0),
                      landscape=False, rotate_180=False)
    text_width = neato.measure_text('Landscape')
    display.draw_text(0, display.height - 1,
                      'Landscape', neato,
                      color565(255, 0, 0),
                      landscape=True, rotate_180=False)
    text_width = neato.measure_text('Portrait Rotate 180')
    display.draw_text(display.width - text_width - 1,
                      display.height - font_height,
                      'Portrait Rotate 180', neato,
                      color565(255, 0, 255),
                      landscape=False, rotate_180=True)
    text_width = neato.measure_text('Landscape Rotate 180')
    display.draw_text(display.width - font_height - 1, text_width,
                      'Landscape Rotate 180', neato,
                      color565(0, 0, 255),
                      landscape=True, rotate_180=True)
    sleep(5)

    # Robotron
    display.clear()
    font_height = robotron.height
    display.draw_text(0, 0,
                      'PORT.', robotron,
                      color565(255, 255, 0),
                      landscape=False, rotate_180=False)
    text_width = robotron.measure_text('LAND.')
    display.draw_text(0, display.height - 1,
                      'LAND.', robotron,
                      color565(255, 0, 0),
                      landscape=True, rotate_180=False)
    text_width = robotron.measure_text('PORT.')
    display.draw_text(display.width - text_width - 1,
                      display.height - font_height,
                      'PORT.', robotron,
                      color565(255, 0, 255),
                      landscape=False, rotate_180=True)
    text_width = robotron.measure_text('ROT. 180')
    display.draw_text(display.width - text_width - 1,
                      display.height - font_height * 2,
                      'ROT. 180', robotron,
                      color565(255, 0, 255),
                      landscape=False, rotate_180=True)
    text_width = robotron.measure_text('LAND.')
    display.draw_text(display.width - font_height - 1, text_width,
                      'LAND.', robotron,
                      color565(0, 0, 255),
                      landscape=True, rotate_180=True)
    text_width = robotron.measure_text('ROT. 180')
    display.draw_text(display.width - font_height * 2 - 1, text_width,
                      'ROT. 180', robotron,
                      color565(0, 0, 255),
                      landscape=True, rotate_180=True)
    sleep(5)

    # Unispace
    display.clear()
    font_height = unispace.height
    display.draw_text(0, 0,
                      'PORT. ', unispace,
                      color565(255, 255, 0),
                      background=color565(255, 0, 0),
                      landscape=False, rotate_180=False)
    text_width = unispace.measure_text('LAND. ')
    display.draw_text(0, display.height - 1,
                      'LAND. ', unispace,
                      color565(255, 0, 0),
                      background=color565(255, 255, 0),
                      landscape=True, rotate_180=False)
    text_width = unispace.measure_text('PORT. ')
    display.draw_text(display.width - text_width - 1,
                      display.height - font_height,
                      'PORT. ', unispace,
                      color565(255, 0, 255),
                      background=color565(0, 255, 0),
                      landscape=False, rotate_180=True)
    text_width = unispace.measure_text('ROT. 180')
    display.draw_text(display.width - text_width - 1,
                      display.height - font_height * 2,
                      'ROT. 180', unispace,
                      color565(255, 0, 255),
                      background=color565(0, 255, 0),
                      landscape=False, rotate_180=True)
    text_width = unispace.measure_text('LAND. ')
    display.draw_text(display.width - font_height - 1, text_width,
                      'LAND. ', unispace,
                      color565(0, 0, 255),
                      background=color565(255, 255, 0),
                      landscape=True, rotate_180=True)
    text_width = unispace.measure_text('ROT. 180')
    display.draw_text(display.width - font_height * 2 - 1, text_width,
                      'ROT. 180', unispace,
                      color565(0, 0, 255),
                      background=color565(255, 255, 0),
                      landscape=True, rotate_180=True)

    sleep(10)
    display.cleanup()


test()
