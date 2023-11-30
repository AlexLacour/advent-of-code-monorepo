from collections import defaultdict

from aoc_utils import read_input

moves = read_input(one_line=True, separator=None)

move_to_coords_dict = {"^": (0, 1), "v": (0, -1), ">": (1, 0), "<": (-1, 0)}


def compute_gifts_map(instructions: str, with_robo_santa: bool = False):
    position = [0, 0]
    robo_santa_position = [0, 0]

    gifts_map_dict = defaultdict(int)

    gifts_map_dict[tuple(position)] += 1
    if with_robo_santa:
        gifts_map_dict[tuple(robo_santa_position)] += 1

    for move_id, move_char in enumerate(instructions):
        if with_robo_santa and move_id % 2:
            position_to_update = robo_santa_position
        else:
            position_to_update = position

        x_move, y_move = move_to_coords_dict[move_char]

        position_to_update[0] += x_move
        position_to_update[1] += y_move

        gifts_map_dict[tuple(position_to_update)] += 1
    return gifts_map_dict


print("P1", len(compute_gifts_map(moves)))
print("P2", len(compute_gifts_map(moves, with_robo_santa=True)))
