import numpy as np

from aoc_utils import read_input

path_instructions = read_input(
    one_line=True, separator=", ", as_type=lambda x: (x[0], int(x[1:]))
)

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def walk_through_instructions(
    instructions: list[tuple], break_if_duplicate: bool = False
) -> tuple:
    positions_buffer = []

    position = np.array((0, 0))
    direction_index = 0
    for rotation, amount in instructions:
        direction_index += 1 if rotation == "R" else -1

        for _ in range(amount):
            position += np.asarray(DIRECTIONS[direction_index % len(DIRECTIONS)])

            if break_if_duplicate and tuple(position) not in positions_buffer:
                positions_buffer.append(tuple(position))
            elif break_if_duplicate:
                return tuple(position)

    return tuple(position)


distance = lambda x: sum(map(abs, x))  # manhattan distance

print(distance(walk_through_instructions(path_instructions)))

print(distance(walk_through_instructions(path_instructions, break_if_duplicate=True)))
