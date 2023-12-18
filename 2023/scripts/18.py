import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
from scipy.ndimage import binary_fill_holes

from aoc_utils import read_input

RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)
DIRECTIONS = {
    "R": RIGHT,
    "L": LEFT,
    "U": UP,
    "D": DOWN
}


def parse_instruction(instruction_str: str) -> tuple:
    direction, amount, color = instruction_str.split()
    return np.array(DIRECTIONS[direction]) * int(amount), color


input_digging_instructions = read_input(as_type=parse_instruction)

position = (0, 0)
path = [position]
for instruction in input_digging_instructions:
    direction, _ = instruction
    position = tuple(position + direction)
    path.append(position)
print(path)
