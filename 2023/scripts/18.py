import matplotlib.pyplot as plt
import numpy as np
import shapely
from matplotlib.path import Path
from scipy.ndimage import binary_fill_holes

from aoc_utils import read_input

RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)
DIRECTIONS = {"R": RIGHT, "L": LEFT, "U": UP, "D": DOWN}
DIRECTION_INT = ["R", "D", "L", "U"]


def parse_instruction(instruction_str: str) -> tuple:
    direction, amount, color = instruction_str.split()
    return np.array(DIRECTIONS[direction]) * int(amount), color.strip("()")


input_digging_instructions = read_input(as_type=parse_instruction)


def get_path(digging_instructions: list, use_color_as_direction: bool = False) -> list:
    position = (0, 0)
    path = [position]
    for instruction in digging_instructions:
        direction, color = instruction

        # for P2
        if use_color_as_direction:
            base_direction = np.array(DIRECTIONS[DIRECTION_INT[int(color[-1])]])
            direction = base_direction * int(color[1:-1], 16)

        position = tuple(position + direction)
        path.append(position)
    return path


polygon = shapely.Polygon(get_path(input_digging_instructions))
print("P1", int(polygon.area + polygon.length // 2 + 1))

polygon = shapely.Polygon(
    get_path(input_digging_instructions, use_color_as_direction=True)
)
print("P2", int(polygon.area + polygon.length // 2 + 1))
