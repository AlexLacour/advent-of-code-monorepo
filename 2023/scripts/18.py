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
    return np.array(DIRECTIONS[direction]), int(amount), color


input_digging_instructions = read_input(as_type=parse_instruction)

position = (0, 0)
path = [position]
for instruction in input_digging_instructions:
    direction, amount, _ = instruction
    for _ in range(amount):
        position = tuple(position + direction)
        path.append(position)

min_h = min(path, key=lambda x: x[0])[0]
min_w = min(path, key=lambda x: x[1])[1]
max_h = max(path, key=lambda x: x[0])[0] + 1
max_w = max(path, key=lambda x: x[1])[1] + 1
dig_map = np.zeros((max_h - min_h, max_w - min_w))
for point in path:
    point = point[0] - min_h, point[1] - min_w
    dig_map[point] = 1

filled_map = binary_fill_holes(dig_map)
print("P1", (filled_map > 0).sum())
