# -*- coding: utf-8 -*-
"""Utility to convert FontEdit files to GLCD format."""
from os import path
import sys


def process_file(font_width, font_height, input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()

            # Case 1: Comment Line
            if line.startswith('//'):
                outfile.write(line + '\n')

            # Case 2: Blank Line
            elif not line:
                continue

            # Case 3: Variable Definition
            elif line.startswith('const'):
                continue

            # Case 4: Variable Closing
            elif line.startswith('};'):
                continue

            # Case 5: Hex Value Lines
            else:
                parts = line.split('//')
                hex_values = parts[0].split(',')
                comment = '//' + parts[1] if len(parts) > 1 else ''

                converted_values = convert_hex_value(
                    [val.strip() for val in hex_values if val.strip()],
                    font_width,
                    font_height)

                outfile.write(', '.join(converted_values) + ', ' +
                              comment + '\n')


def hex_to_matrix(hex_values, font_width, font_height):
    # Strip '0x' prefix and filter out invalid hex values
    hex_values = [hv[2:] for hv in hex_values if hv.startswith('0x') and
                  all(c in '0123456789ABCDEFabcdef' for c in hv[2:])]

    # Calculate the number of hex values per row
    values_per_row = font_width // 8 + (1 if font_width % 8 != 0 else 0)

    # Group hex values into rows based on values_per_row
    rows = [hex_values[i:i + values_per_row] for i in range(
        0, len(hex_values), values_per_row)]

    # Verify the number of rows matches the expected font_height
    if len(rows) != font_height:
        raise ValueError(f"Expected {font_height} rows, but found {len(rows)}")

    # Convert grouped hex values to binary rows
    binary_matrix = []
    for row in rows:
        binary_row = ''
        for hv in row:
            # Reverse the order of bits in each byte
            binary_byte = format(int(hv, 16), '08b')[::-1]
            binary_row += binary_byte
        binary_matrix.append(binary_row[:font_width])
    return binary_matrix


def pad_matrix(matrix, font_width, font_height):
    # Calculate the required height to make it divisible by 8
    required_height = ((font_height + 7) // 8) * 8

    # Pad the matrix with rows of zeros if needed
    while len(matrix) < required_height:
        binary_row = '0' * font_width
        matrix.append(list(binary_row))  # Append a list of zeros
    return matrix


def convert_hex_value(hex_values, font_width, font_height):
    # Convert hex values to a binary matrix
    matrix = hex_to_matrix(hex_values, font_width, font_height)
    """
    for row in matrix:
        print(' '.join(row))
    print("---------------")
    """
    # Pad matrix along bottom to be divisible by 8
    matrix = pad_matrix(matrix, font_width, font_height)
    """
    for row in matrix:
        print(' '.join(row))
    """
    return matrix_transposed_to_hex_values(matrix, font_width, font_height)


def matrix_transposed_to_hex_values(matrix, font_width, font_height):
    hex_values = []
    # Convert and prepend the width of the character
    width_hex = '0x' + format(font_width, '02X')
    hex_values.append(width_hex)
    for col in range(font_width):
        for row in range(0, font_height, 8):
            # Extract a group of 8 pixels
            pixel_group = [matrix[r][col] for r in range(row, row + 8)]
            # Convert to binary string in little endian format
            binary_str = ''.join(pixel_group[::-1])
            # Convert binary string to hex value
            hex_value = '0x' + format(int(binary_str, 2), '02X')
            hex_values.append(hex_value)
    return hex_values


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 4:
        error('Please specify font width, height & input file: ./fontedit2glcd.py 24 42 myfont.c')
    width = int(args[1])
    height = int(args[2])
    in_path = args[3]

    if not (1 <= width <= 254):
        error("Width is not between 1 and 254.")

    if not (1 <= height <= 254):
        error("Height is not between 1 and 254.")

    if not path.exists(in_path):
        error('File Not Found: ' + in_path)

    filename, ext = path.splitext(in_path)
    out_path = filename + "_converted" + ext

    process_file(width, height, in_path, out_path)
