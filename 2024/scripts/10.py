from collections import defaultdict
import numpy as np
from aoc_utils import read_input
from aoc_utils.enums.directions import NPArray4Directions
from queue import Queue


def get_next_moves(
    topographic_map: np.ndarray, pos: tuple[int, int]
) -> list[tuple[int, int]]:
    moves = [np.asarray(pos) + move for move in NPArray4Directions.to_list()]

    filtered_moves = [
        tuple(move)
        for move in moves
        if all(0 <= val < topographic_map.shape[axis] for axis, val in enumerate(move))
        and (topographic_map[tuple(move)] - topographic_map[tuple(pos)]) == 1
    ]

    return filtered_moves


input_topographic_map = read_input(as_type=list, to_numpy=True, np_dtype=int)
trailheads = np.argwhere(input_topographic_map == 0)

# part 1
trailheads_ends = defaultdict(set)
# part 2
trailheads_ratings = defaultdict(int)

for trailhead in trailheads:
    trail_positions = Queue()
    trail_positions.put(trailhead.copy())

    n_paths = 1

    while trail_positions.qsize():
        queued_position = trail_positions.get()
        new_positions = get_next_moves(input_topographic_map, queued_position)

        if len(new_positions) > 1:
            n_paths += len(new_positions) - 1
        elif not new_positions and input_topographic_map[tuple(queued_position)] != 9:
            n_paths -= 1

        for position in new_positions:
            if input_topographic_map[tuple(position)] == 9:
                trailheads_ends[tuple(trailhead)].add(tuple(position))
            trail_positions.put(position)

    trailheads_ratings[tuple(trailhead)] = n_paths

trailheads_scores = {
    trailhead: len(ends) for trailhead, ends in trailheads_ends.items()
}
print(f"{sum(trailheads_scores.values())=}")

print(f"{sum(trailheads_ratings.values())=}")
