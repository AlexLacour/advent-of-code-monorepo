import numpy as np
from aoc_utils import read_input
import shapely


def parse_coordinate(yx_str: str) -> tuple[int, ...]:
    return tuple(map(int, yx_str.split(",")))


def rect_area(x1: int, y1: int, x2: int, y2: int) -> int:
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


input_red_tiles = read_input(as_type=parse_coordinate)

full_area = shapely.Polygon(input_red_tiles)

max_area = 0
for pid, p1 in enumerate(input_red_tiles):
    for p2 in input_red_tiles[pid:]:
        # area = rect_area(*p1, *p2)

        x1, y1 = p1
        x2, y2 = p2
        xmin, xmax = min(x1, x2), max(x1, x2)
        ymin, ymax = min(y1, y2), max(y1, y2)

        rectangle = shapely.Polygon(
            [(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)]
        )

        if rectangle.within(full_area):
            max_area = max(rect_area(*p1, *p2), max_area)
print(max_area)
