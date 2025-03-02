"""ILI9341 demo (fonts)."""
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
    print('Loading bally')
    bally = XglcdFont('fonts/Bally7x9.c', 7, 9)
    print('Loading broadway')
    broadway = XglcdFont('fonts/Broadway17x15.c', 17, 15)
    print('Loading espresso_dolce')
    espresso_dolce = XglcdFont('fonts/EspressoDolce18x24.c', 18, 24)
    print('Loading fixed_font')
    fixed_font = XglcdFont('fonts/FixedFont5x8.c', 5, 8)
    print('Loading neato')
    neato = XglcdFont('fonts/Neato5x7.c', 5, 7, letter_count=223)
    print('Loading robotron')
    robotron = XglcdFont('fonts/Robotron13x21.c', 13, 21)
    print('Loading unispace')
    unispace = XglcdFont('fonts/Unispace12x24.c', 12, 24)
    print('Loading wendy')
    wendy = XglcdFont('fonts/Wendy7x8.c', 7, 8)
    print('Fonts loaded.')

    text_heights = [11, 9, 15, 24, 8, 7, 21, 24, 8]  # Heights of each line
    num_lines = len(text_heights)  # Number of lines
    total_text_height = sum(text_heights)  # Total height of all text lines
    # Calculate available space to distribute
    available_height = display.height - total_text_height
    # Calculate the vertical gap between each line
    gap_between_lines = available_height // (num_lines + 1)
    # Start drawing the text at the first position
    y_position = gap_between_lines  # Start of first line of text
    # Draw each text line with adjusted Y positions
    display.draw_text(0, y_position, 'Arcade Pix 9x11', arcadepix,
                      color565(255, 0, 0))
    y_position += text_heights[0] + gap_between_lines
    display.draw_text(0, y_position, 'Bally 7x9', bally, color565(0, 255, 0))
    y_position += text_heights[1] + gap_between_lines
    display.draw_text(0, y_position, 'Broadway', broadway,
                      color565(0, 0, 255))
    y_position += text_heights[2] + gap_between_lines
    display.draw_text(0, y_position, 'Espresso', espresso_dolce,
                      color565(0, 255, 255))
    y_position += text_heights[3] + gap_between_lines
    display.draw_text(0, y_position, 'Fixed Font 5x8', fixed_font,
                      color565(255, 0, 255))
    y_position += text_heights[4] + gap_between_lines
    display.draw_text(0, y_position, 'Neato 5x7', neato, color565(255, 255, 0))
    y_position += text_heights[5] + gap_between_lines
    display.draw_text(0, y_position, 'ROBOTRON', robotron,
                      color565(255, 255, 255))
    y_position += text_heights[6] + gap_between_lines
    display.draw_text(0, y_position, 'Unispace', unispace,
                      color565(255, 128, 0))
    y_position += text_heights[7] + gap_between_lines
    display.draw_text(0, y_position, 'Wendy 7x8', wendy, color565(255, 0, 128))
    sleep(9)

    display.clear()
    y_position = gap_between_lines  # Start of first line of text
    display.draw_text(0, y_position, 'Arcade Pix 9x11', arcadepix,
                      color565(255, 0, 0), background=color565(0, 255, 255))
    y_position += text_heights[0] + gap_between_lines
    display.draw_text(0, y_position, 'Bally 7x9', bally,
                      color565(0, 255, 0), background=color565(0, 0, 128))
    y_position += text_heights[1] + gap_between_lines
    display.draw_text(0, y_position, 'Broadway', broadway,
                      color565(0, 0, 255), background=color565(255, 255, 0))
    y_position += text_heights[2] + gap_between_lines
    display.draw_text(0, y_position, 'Espresso', espresso_dolce,
                      color565(0, 255, 255), background=color565(255, 0, 0))
    y_position += text_heights[3] + gap_between_lines
    display.draw_text(0, y_position, 'Fixed Font 5x8', fixed_font,
                      color565(255, 0, 255), background=color565(0, 128, 0))
    y_position += text_heights[4] + gap_between_lines
    display.draw_text(0, y_position, 'Neato 5x7', neato,
                      color565(255, 255, 0), background=color565(0, 0, 255))
    y_position += text_heights[5] + gap_between_lines
    display.draw_text(0, y_position, 'ROBOTRON', robotron,
                      color565(255, 255, 255),
                      background=color565(128, 128, 128))
    y_position += text_heights[6] + gap_between_lines
    display.draw_text(0, y_position, 'Unispace', unispace,
                      color565(255, 128, 0), background=color565(0, 128, 255))
    y_position += text_heights[7] + gap_between_lines
    display.draw_text(0, y_position, 'Wendy 7x8', wendy,
                      color565(255, 0, 128),
                      background=color565(255, 255, 255))
    sleep(9)

    display.clear()
    # Calculate available horizontal space
    available_width = display.width - total_text_height
    # Calculate the horizontal gap between each line
    gap_between_lines = available_width // (num_lines + 1)
    # Starting X position for each line
    x_position = gap_between_lines
    # Draw each text line with adjusted X positions
    display.draw_text(x_position, display.height - 1, 'Arcade Pix 9x11',
                      arcadepix, color565(255, 0, 0), landscape=True)
    x_position += text_heights[0] + gap_between_lines
    display.draw_text(x_position, display.height - 1, 'Bally 7x9', bally,
                      color565(0, 255, 0), landscape=True)
    x_position += text_heights[1] + gap_between_lines
    display.draw_text(x_position, display.height - 1, 'Broadway 17x15',
                      broadway, color565(0, 0, 255), landscape=True)
    x_position += text_heights[2] + gap_between_lines
    display.draw_text(x_position, display.height - 1, 'Espresso',
                      espresso_dolce, color565(0, 255, 255), landscape=True)
    x_position += text_heights[3] + gap_between_lines
    display.draw_text(x_position, display.height - 1, 'Fixed Font 5x8',
                      fixed_font, color565(255, 0, 255), landscape=True)
    x_position += text_heights[4] + gap_between_lines
    display.draw_text(x_position, display.height - 1, 'Neato 5x7', neato,
                      color565(255, 255, 0), landscape=True)
    x_position += text_heights[5] + gap_between_lines
    display.draw_text(x_position, display.height - 1, 'ROBOTRON',
                      robotron, color565(255, 255, 255), landscape=True)
    x_position += text_heights[6] + gap_between_lines
    display.draw_text(x_position, display.height - 1, 'Unispace',
                      unispace, color565(255, 128, 0), landscape=True)
    x_position += text_heights[7] + gap_between_lines
    display.draw_text(x_position, display.height - 1, 'Wendy 7x8', wendy,
                      color565(255, 0, 128), landscape=True)
    sleep(9)
    display.cleanup()


test()
