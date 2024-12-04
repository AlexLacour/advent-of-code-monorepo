import numpy as np

from aoc_utils import read_input
from aoc_utils.enums.directions import NPArray4Directions

DIRECTIONS_MAPPING = {
    "U": NPArray4Directions.UP,
    "D": NPArray4Directions.DOWN,
    "L": NPArray4Directions.LEFT,
    "R": NPArray4Directions.RIGHT
}

KEYS_MAPPING = {
    10: "A",
    11: "B",
    12: "C",
    13: "D"
}


code_instructions = read_input()

first_panel = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

second_panel = np.array([
    [0, 0, 1, 0, 0],
    [0, 2, 3, 4, 0],
    [5, 6, 7, 8, 9],
    [0, 10, 11, 12, 0],
    [0, 0, 13, 0, 0]
])


def get_code(instructions: list[str], panel: np.ndarray, starting_key: int = 5) -> str:
    code = ""

    position = list(zip(*np.where(panel == starting_key)))[0]
    key = starting_key

    for digit_instructions in instructions:
        for direction_str in digit_instructions:
            new_position = position + DIRECTIONS_MAPPING[direction_str]

            if not any(val < 0 or val > len(panel) - 1 for val in new_position) and panel[tuple(new_position)] != 0:
                key = panel[tuple(new_position)]
                position = new_position
        code += str(key) if key < 10 else KEYS_MAPPING[key]
    
    return code


print(get_code(code_instructions, first_panel))
print(get_code(code_instructions, second_panel))
