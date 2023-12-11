from itertools import combinations

import numpy as np
from scipy.spatial.distance import cdist

from aoc_utils import read_input

input_galaxies_map = read_input(as_type=list, to_numpy=True)


# NOTE : deprecated
def expand_galaxies_map(
    galaxies_map: np.ndarray,
) -> np.ndarray:  # Funny but useless in the end
    # expand rows
    empty_rows_ids = [
        row_id for row_id, row in enumerate(galaxies_map) if "#" not in row
    ]
    galaxies_map = np.insert(
        galaxies_map, empty_rows_ids, ["." * len(galaxies_map[0])], 0
    )

    # expand cols
    empty_cols_ids = [
        col_id for col_id, col in enumerate(galaxies_map.T) if "#" not in col
    ]

    galaxies_map = np.insert(galaxies_map, empty_cols_ids, ["." * len(galaxies_map)], 1)

    return galaxies_map


def expand_galaxies_coordinates(
    galaxies_map: np.ndarray, expansion_size: int
) -> list[tuple]:
    empty_rows_ids = [
        row_id for row_id, row in enumerate(galaxies_map) if "#" not in row
    ]
    empty_cols_ids = [
        col_id for col_id, col in enumerate(galaxies_map.T) if "#" not in col
    ]

    galaxies_coordinates = list(zip(*np.where(galaxies_map == "#")))

    expanded_coordinates = []
    for coords in galaxies_coordinates:
        row_coord, col_coord = coords

        above_empty_rows = [row_id for row_id in empty_rows_ids if row_coord > row_id]
        row_coord += len(above_empty_rows) * expansion_size
        above_empty_cols = [col_id for col_id in empty_cols_ids if col_coord > col_id]
        col_coord += len(above_empty_cols) * expansion_size

        expanded_coordinates.append((row_coord, col_coord))

    return expanded_coordinates


def get_galaxies_distances_sum(
    galaxies_map: np.ndarray, expansion_size: int = 1
) -> int:
    # expanded_galaxies_map = expand_galaxies_map(galaxies_map)
    # galaxies_coordinates = list(zip(*np.where(expanded_galaxies_map == "#")))
    galaxies_coordinates = expand_galaxies_coordinates(galaxies_map, expansion_size)

    galaxies_coordinates_to_id = {
        coords: galaxy_id for galaxy_id, coords in enumerate(galaxies_coordinates)
    }
    np_galaxies_coordinates = np.array(list(galaxies_coordinates_to_id.keys()))
    distances = cdist(
        np_galaxies_coordinates, np_galaxies_coordinates, metric="cityblock"
    )

    galaxy_pairs = list(combinations(galaxies_coordinates_to_id, 2))

    distances_sum = sum(
        distances[
            galaxies_coordinates_to_id[first_galaxy],
            galaxies_coordinates_to_id[second_galaxy],
        ]
        for first_galaxy, second_galaxy in galaxy_pairs
    )

    return int(distances_sum)


print("P1", get_galaxies_distances_sum(input_galaxies_map, expansion_size=1))
print("P2", get_galaxies_distances_sum(input_galaxies_map, expansion_size=999_999))
