from collections import defaultdict
import copy
import numpy as np
from aoc_utils import read_input
from aoc_utils.enums.directions import NPArray4Directions

input_map = read_input(as_type=list, to_numpy=True)

# guard constants
GUARD_STEP_ORDER = "^>v<"
GUARD_STEP_DIRECTION = {
    "^": tuple(NPArray4Directions.UP),
    ">": tuple(NPArray4Directions.RIGHT),
    "v": tuple(NPArray4Directions.DOWN),
    "<": tuple(NPArray4Directions.LEFT),
}
OBSTACLE = "#"


def run_guard_patrol(
    lab_map: np.ndarray,
    starting_point: tuple[int, int],
    guard_step_order_index: int = 0,
) -> set:
    guard_position = np.array(starting_point)

    obstacles_positions_set = set(
        [tuple(obs) for obs in np.argwhere(lab_map == OBSTACLE)]
    )

    visited_with_direction = set()

    while True:
        movement_direction = GUARD_STEP_DIRECTION[
            GUARD_STEP_ORDER[guard_step_order_index]
        ]

        visited_with_direction.add((tuple(guard_position), tuple(movement_direction)))

        while tuple(guard_position + movement_direction) not in obstacles_positions_set:
            guard_position += movement_direction

            if any(
                coord < 0 or coord >= lab_map.shape[axis]
                for axis, coord in enumerate(guard_position)
            ):
                return visited_with_direction

            if (
                tuple(guard_position),
                tuple(movement_direction),
            ) in visited_with_direction:
                raise ValueError

            visited_with_direction.add(
                (tuple(guard_position), tuple(movement_direction))
            )

        guard_step_order_index = (guard_step_order_index + 1) % len(GUARD_STEP_ORDER)


# script
guard_starting_position = tuple(np.argwhere(input_map == GUARD_STEP_ORDER[0])[0])

# part 1
visited_points = run_guard_patrol(
    copy.deepcopy(input_map), starting_point=guard_starting_position
)
visited_points_coords = set([x[0] for x in visited_points])
print(f"{len(visited_points_coords)=}")

# part 2
loop_counter = 0
for point in visited_points_coords:
    map_copy = copy.deepcopy(input_map)
    map_copy[point] = OBSTACLE

    try:
        run_guard_patrol(map_copy, guard_starting_position)
    except ValueError:
        loop_counter += 1

print(f"{loop_counter=}")
