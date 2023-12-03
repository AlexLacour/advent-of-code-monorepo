import math
import uuid
from collections import defaultdict
from typing import Optional

import numpy as np

from aoc_utils import read_input

input_engine_schematic = read_input()


def part1(engine_schematic: list) -> dict:
    numbers = {}
    digit_start = False
    coords_to_check = set()
    computed_sum = 0

    for line_id, symbol_line in enumerate(engine_schematic):
        for col_id, potential_symbol in enumerate(symbol_line):
            if potential_symbol.isdigit():
                if not digit_start:
                    new_number = []
                    coords_to_check = set()
                    digit_start = True
                if digit_start:
                    new_number.append(potential_symbol)
                    for coord in get_square_around_coord((line_id, col_id), len(engine_schematic), len(engine_schematic[0])):
                        coords_to_check.add(coord)

            else:
                if digit_start:
                    digit_start = False
                    number_int = int("".join(new_number))
                    numbers[(line_id, col_id - 1)] = number_int

                    for coord in coords_to_check:
                        if is_coord_symbol(engine_schematic, coord):
                            computed_sum += number_int
                            break

    return computed_sum


def get_square_around_coord(coordinate: tuple, n_lines: int, n_cols: int) -> set[tuple]:
    coordinates_to_check = set()
    coord_modifiers = set([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])

    for mod in coord_modifiers:
        candidate = (coordinate[0] + mod[0], coordinate[1] + mod[1])

        if 0 <= candidate[0] < n_lines and 0 <= candidate[1] < n_cols:
            coordinates_to_check.add(candidate)
    return coordinates_to_check


def is_coord_symbol(engine_schematic: list, coordinate: tuple, value: Optional[str] = None) -> bool:
    potential_symbol = engine_schematic[coordinate[0]][coordinate[1]]
    if potential_symbol != "." and not potential_symbol.isdigit():
        if not value or potential_symbol == value:
            return True
    return False


def part2(engine_schematic: list) -> dict:
    numbers = {}
    digit_start = False
    coords_to_check = set()
    
    gears = defaultdict(list)

    for line_id, symbol_line in enumerate(engine_schematic):
        for col_id, potential_symbol in enumerate(symbol_line):
            if potential_symbol.isdigit():
                if not digit_start:
                    new_number = []
                    coords_to_check = set()
                    digit_start = True
                if digit_start:
                    new_number.append(potential_symbol)
                    for coord in get_square_around_coord((line_id, col_id), len(engine_schematic), len(engine_schematic[0])):
                        coords_to_check.add(coord)

            else:
                if digit_start:
                    digit_start = False
                    number_int = int("".join(new_number))
                    numbers[(line_id, col_id - 1)] = number_int

                    for coord in coords_to_check:
                        if is_coord_symbol(engine_schematic, coord, value="*"):
                            gears[coord].append(number_int)

    gears = {coord: nums for coord, nums in gears.items() if len(nums) == 2} 

    ratio_sum = sum([math.prod(nums) for nums in gears.values()])

    return ratio_sum

print("P1", part1(input_engine_schematic))
print("P2", part2(input_engine_schematic))
