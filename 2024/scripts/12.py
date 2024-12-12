from collections import defaultdict
from aoc_utils import read_input
import numpy as np
from aoc_utils.enums.directions import NPArray4Directions, NPArray8Directions
from scipy.ndimage import label
from itertools import combinations


input_regions = read_input(as_type=list, to_numpy=True)

region_names = np.unique(input_regions)

total_price = 0
total_deal_price = 0
for region_name in region_names:
    regions_coordinates = [
        tuple(coord) for coord in np.argwhere(input_regions == region_name)
    ]

    labeled_regions, n_regions = label(input_regions == region_name)
    for region_id in range(n_regions):
        new_region = [
            tuple(coord) for coord in np.argwhere(labeled_regions == region_id + 1)
        ]

        # stats
        area = len(new_region)
        points_outside_contacts = {
            point: sum(
                [
                    any(
                        val < 0 or val >= labeled_regions.shape[axis]
                        for axis, val in enumerate(tuple(direction + point))
                    )
                    or labeled_regions[tuple(direction + point)] != region_id + 1
                    for direction in NPArray4Directions.to_list()
                ]
            )
            for point in new_region
        }
        perimeter = sum(points_outside_contacts.values())

        # n_sides
        n_corners = 0
        ortho_pairs = [
            (NPArray4Directions.UP, NPArray4Directions.RIGHT),
            (NPArray4Directions.UP, NPArray4Directions.LEFT),
            (NPArray4Directions.DOWN, NPArray4Directions.RIGHT),
            (NPArray4Directions.DOWN, NPArray4Directions.LEFT),
        ]

        for point in new_region:
            for ortho_pair in ortho_pairs:
                non_matching_neighbors = [
                    tuple(direction + point)
                    for direction in ortho_pair
                    if any(
                        val < 0 or val >= labeled_regions.shape[axis]
                        for axis, val in enumerate(tuple(direction + point))
                    )
                    or labeled_regions[tuple(direction + point)] != region_id + 1
                ]

                if len(non_matching_neighbors) == 2:
                    n_corners += 1

                elif not non_matching_neighbors and (
                    any(
                        val < 0 or val >= labeled_regions.shape[axis]
                        for axis, val in enumerate(tuple(sum(ortho_pair) + point))
                    )
                    or labeled_regions[tuple(sum(ortho_pair) + point)] != region_id + 1
                ):
                    n_corners += 1

        total_price += area * perimeter
        total_deal_price += area * n_corners

print(f"{total_price=}")
print(f"{total_deal_price=}")
