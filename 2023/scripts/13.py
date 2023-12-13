from typing import Optional

import numpy as np

from aoc_utils import read_input

input_patterns = read_input(as_type=list)

input_np_patterns = [[]]
for pattern_line in input_patterns:
    if not pattern_line:
        input_np_patterns.append([])
    else:
        input_np_patterns[-1].append(pattern_line)
input_np_patterns = [np.array(subarray) for subarray in input_np_patterns]


def find_symetry_axis(
    pattern: np.ndarray, fix_smudge: bool = True
) -> Optional[tuple[int, int]]:
    height, _ = pattern.shape
    for line_id, _ in enumerate(pattern[:-1]):
        min_len = min(line_id + 1, height - (line_id + 1))
        above = pattern[: line_id + 1][-min_len:]
        below = pattern[line_id + 1 :][:min_len][::-1]

        if (
            not fix_smudge
            and np.array_equal(above, below)
            or fix_smudge
            and len(np.where((above != below) == True)[0]) == 1
        ):
            return line_id + 1
    return 0


def get_all_sym_axis(patterns: list, fix_smudge: bool = False) -> tuple[int, int]:
    n_rows = 0
    n_cols = 0
    for pattern in patterns:
        n_rows += find_symetry_axis(pattern, fix_smudge=fix_smudge)
        n_cols += find_symetry_axis(pattern.T, fix_smudge=fix_smudge)
    return n_rows, n_cols


print(
    "P1",
    sum(
        [
            value * weight
            for value, weight in zip(
                get_all_sym_axis(input_np_patterns, False), (100, 1)
            )
        ]
    ),
)
print(
    "P2",
    sum(
        [
            value * weight
            for value, weight in zip(
                get_all_sym_axis(input_np_patterns, True), (100, 1)
            )
        ]
    ),
)
