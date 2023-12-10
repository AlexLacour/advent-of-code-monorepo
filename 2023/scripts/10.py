import numpy as np
from matplotlib.path import Path

from aoc_utils import read_input

# PIPE_TO_INT = [c for c in ".|-LJ7FS"]

PIPE_DIRECTION = {
    ".": [],
    "|": [[-1, 0], [1, 0]],  # up down
    "-": [[0, -1], [0, 1]],  # left right
    "L": [[-1, 0], [0, 1]],  # up right
    "J": [[0, -1], [-1, 0]],  # left up
    "7": [[0, -1], [1, 0]],  # left down
    "F": [[1, 0], [0, 1]],  # down right
    "S": [[0, -1], [0, 1], [-1, 0], [1, 0]],  # all
}

input_pipes = read_input(as_type=list, to_numpy=True)


def get_adjacent_pipe_positions(pipes: list, position: tuple) -> list[tuple]:
    position_line, position_col = position
    value_str = pipes[position_line][position_col]

    candidates = []
    for direction in PIPE_DIRECTION[value_str]:
        candidate = (position_line + direction[0], position_col + direction[1])

        if 0 <= candidate[0] < len(pipes) and 0 <= candidate[1] < len(pipes[0]):
            candidates.append(candidate)

    return candidates


# Get S
starting_position = None
for line_id, line in enumerate(input_pipes):
    for col_id, value in enumerate(line):
        if value == "S":
            starting_position = (line_id, col_id)

loop_positions = [starting_position]
candidates = get_adjacent_pipe_positions(input_pipes, starting_position)
for valid_candidate in candidates:
    if starting_position in get_adjacent_pipe_positions(input_pipes, valid_candidate):
        loop_positions.append(valid_candidate)

last_position = starting_position
position = loop_positions[-1]  # NOTE either 1 or -1, can somehow change things

while position != starting_position:
    position_value_str = input_pipes[position]

    for possible_point_difference in PIPE_DIRECTION[position_value_str]:
        potential_next_point = tuple(np.asarray(position) + possible_point_difference)
        if potential_next_point != last_position:
            break

    last_position = position
    position = potential_next_point

    loop_positions.append(position)


print("P1", len(set(loop_positions)) // 2)

loop = Path(loop_positions, closed=True)
filled_in = 0
for point_value in (it := np.nditer(input_pipes, flags=["multi_index"])):
    point_coords = it.multi_index

    if point_coords not in loop_positions and loop.contains_point(point_coords):
        filled_in += 1

print("P2", filled_in)
