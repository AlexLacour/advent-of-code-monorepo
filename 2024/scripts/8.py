import copy
from typing import Optional
from aoc_utils import read_input
import numpy as np
from itertools import combinations


input_antenna_map = read_input(as_type=list, to_numpy=True)


def get_antinodes(
    antenna_map: np.ndarray, antinodes_limit: Optional[int] = None
) -> set:
    # setup
    antenna_locations = np.argwhere(antenna_map != ".")

    antenna_location_to_frequency: dict[tuple[int, int], str] = {
        tuple(location): antenna_map[tuple(location)] for location in antenna_locations
    }
    antenna_frequency_to_locations: dict[str, list[np.ndarray]] = {
        searched_frequency: [
            np.asarray(location)
            for location, frequency in antenna_location_to_frequency.items()
            if frequency == searched_frequency
        ]
        for searched_frequency in antenna_location_to_frequency.values()
    }

    # search
    antinodes = []
    for _, locations in antenna_frequency_to_locations.items():
        antenna_pairs = combinations(locations, r=2)

        for pair in antenna_pairs:
            pair_vector = pair[1] - pair[0]

            left_antinodes = []  # left of the first location (substract the vector)
            right_antinodes = []  # right of the second location (add the vector)

            right_antinode = pair[1].copy()
            while True:
                right_antinode += pair_vector

                if not any(
                    val < 0 or val >= antenna_map.shape[axis]
                    for axis, val in enumerate(right_antinode)
                ):
                    right_antinodes.append(tuple(right_antinode))
                else:
                    break

            left_antinode = pair[0].copy()
            while True:
                left_antinode -= pair_vector

                if not any(
                    val < 0 or val >= antenna_map.shape[axis]
                    for axis, val in enumerate(left_antinode)
                ):
                    left_antinodes.append(tuple(left_antinode))
                else:
                    break

            if antinodes_limit is None:
                antinodes.extend(
                    [*left_antinodes, *right_antinodes, tuple(pair[0]), tuple(pair[1])]
                )
            else:
                antinodes.extend(
                    [
                        *left_antinodes[:antinodes_limit],
                        *right_antinodes[:antinodes_limit],
                    ]
                )

    return set(antinodes)


print(f"{len(get_antinodes(input_antenna_map, antinodes_limit=1))=}")
print(f"{len(get_antinodes(input_antenna_map, antinodes_limit=None))=}")
