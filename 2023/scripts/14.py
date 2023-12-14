import copy
import hashlib
from typing import Optional

import numpy as np
from tqdm import tqdm

from aoc_utils import read_input

input_rocks_map = read_input(as_type=list, to_numpy=True)

DIRECTIONS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}


def move_rocks(static_rocks: set, movable_rocks: dict, direction: str) -> set[tuple]:
    new_static_rocks = set()

    while any(val is not None for val in movable_rocks.values()):
        for rock_id, rock in movable_rocks.items():
            if rock is None:
                continue
            potential_new_position = rock + DIRECTIONS[direction]
            if (
                not 0 <= potential_new_position[0] < len(input_rocks_map)
                or not 0 <= potential_new_position[1] < len(input_rocks_map[0])
                or tuple(potential_new_position) in static_rocks
                or tuple(potential_new_position) in new_static_rocks
            ):
                new_static_rocks.add(tuple(rock))
                movable_rocks[rock_id] = None
            else:
                movable_rocks[rock_id] = potential_new_position
    return new_static_rocks


def get_load(initial_rocks_map: np.ndarray, directions: list[str], n_cycles: int = 1) -> int:
    height, width = initial_rocks_map.shape

    initial_movable_rocks = {
        rock_id: np.array((x, y))
        for rock_id, (x, y) in enumerate(zip(*np.where(initial_rocks_map == "O")))
    }

    static_rocks = set(
        [(x, y) for x, y in zip(*np.where(initial_rocks_map == "#"))]
    )

    movable_rocks = copy.deepcopy(initial_movable_rocks)
    for i in tqdm(range(n_cycles)):
        for direction in directions:

            movable_rocks_set = move_rocks(static_rocks, copy.deepcopy(movable_rocks), direction)
            movable_rocks = {rock_id: np.array(rock_pos) for rock_id, rock_pos in enumerate(movable_rocks_set)}

    result = sum(height - (rock[0]) for rock in movable_rocks.values())

    return result



print("P1", get_load(input_rocks_map, directions=["N"]))
# print("P2", get_load(input_rocks_map, directions=["N", "W", "S", "E"], n_cycles=1000000000))