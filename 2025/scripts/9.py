import numpy as np
from aoc_utils import read_input


def parse_coordinate(yx_str: str) -> tuple[int, ...]:
    return tuple(map(int, yx_str.split(",")))


input_red_tiles = read_input(as_type=parse_coordinate)

max_area = 0
for pid, p1 in enumerate(input_red_tiles):
    for p2 in input_red_tiles[pid:]:
        area = (abs(p2[0] - p1[0]) + 1) * (abs(p2[1] - p1[1]) + 1)

        max_area = max(area, max_area)
print(max_area)
