from collections import defaultdict
from aoc_utils import read_input
import re
import itertools


def _parse_string(box_str: str) -> tuple[int, ...]:
    res = re.split(r"[#@:,x]", box_str)
    return tuple(map(int, res[1:]))


input_rectangles = read_input(as_type=_parse_string)
claimed_points = defaultdict(set)

fabric_candidates = set([rect[0] for rect in input_rectangles])

for _id, x, y, w, h in input_rectangles:
    x_range = range(x, x + w)
    y_range = range(y, y + h)
    for point in itertools.product(x_range, y_range):
        if point in claimed_points:
            ids_to_remove = [_id, *claimed_points[point]]
            for id_to_remove in ids_to_remove:
                fabric_candidates.discard(id_to_remove)
        claimed_points[point].add(_id)

overlap_surface = sum([1 if len(v) > 1 else 0 for v in claimed_points.values()])
print(overlap_surface)
print(fabric_candidates)
