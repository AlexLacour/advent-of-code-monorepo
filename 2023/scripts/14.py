import copy
import hashlib
from collections import Counter, defaultdict
from typing import Optional

import numpy as np
from tqdm import tqdm

from aoc_utils import read_input

input_rocks_map = read_input(as_type=list, to_numpy=True)


def move_rocks(rocks_map: np.ndarray):
    rocks_position = sorted(
        [(line, col) for line, col in zip(*np.where(rocks_map == "O"))]
    )

    for rock in rocks_position:
        line, col = rock
        above = rocks_map[:line, col][::-1]

        n_moves = 0
        for c in above:
            if c != ".":
                break
            n_moves += 1

        rocks_map[line, col] = "."  # start moving
        rocks_map[line - n_moves, col] = "O"
    return rocks_map


def get_load(rocks_map: np.ndarray):
    height, _ = rocks_map.shape
    return sum(
        height - pos[0]
        for pos in [(line, col) for line, col in zip(*np.where(rocks_map == "O"))]
    )


def run_cycle(rocks_map: np.ndarray) -> np.ndarray:
    for _ in ["N", "W", "S", "E"]:  # counter clockwise
        rocks_map = np.rot90(move_rocks(rocks_map), axes=(1, 0))
    return rocks_map


print("P1", get_load(move_rocks(input_rocks_map)))

n_cycles = 1000000000
maps_history = []
rocks_map = input_rocks_map
period = 0
offset = 0
loads = []
for cycle_id in range(n_cycles):
    rocks_map = run_cycle(rocks_map)
    loads.append(get_load(rocks_map))

    rocks_map_str = "".join(str(el) for el in np.nditer(rocks_map))
    if not rocks_map_str in maps_history:
        maps_history.append(rocks_map_str)
    else:
        last_seen_id = maps_history.index(rocks_map_str)
        period = cycle_id - last_seen_id
        offset = cycle_id - period  # time before the period starts
        loads = loads[-period - 1 : -1]  # only the non repeating part
        break

load_index = (n_cycles - offset) % period
print("P2", loads[load_index - 1])
