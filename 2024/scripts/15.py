import os
import sys
from typing import Optional
import numpy as np
from aoc_utils import read_input
from aoc_utils.enums.directions import NPArray4Directions

DIRECTIONS_MAPPING = {
    "^": NPArray4Directions.UP,
    ">": NPArray4Directions.RIGHT,
    "v": NPArray4Directions.DOWN,
    "<": NPArray4Directions.LEFT,
}

ROBOT_TOKEN = "@"
BOX_TOKEN = "O"
WALL_TOKEN = "#"
EMPTY_TOKEN = "."


def attempt_move(
    warehouse_map: np.ndarray, position: np.ndarray, move: np.ndarray
) -> Optional[np.ndarray]:
    next_position = position + move

    if warehouse_map[tuple(next_position)] == BOX_TOKEN:
        # move boxes if possible
        new_box_position = attempt_move(warehouse_map, next_position, move)
        if new_box_position is not None:

            warehouse_map[tuple(next_position)] = warehouse_map[tuple(position)]
            warehouse_map[tuple(position)] = EMPTY_TOKEN

            return next_position

    elif warehouse_map[tuple(next_position)] != WALL_TOKEN:
        warehouse_map[tuple(next_position)] = warehouse_map[tuple(position)]
        warehouse_map[tuple(position)] = EMPTY_TOKEN
        return next_position


def attempt_move_wider(
    warehouse_map: np.ndarray,
    position: np.ndarray,
    move: np.ndarray,
    update_map: bool = True,
    boxes_to_move: Optional[list] = None,
) -> Optional[np.ndarray]:
    next_position = position + move

    if warehouse_map[tuple(next_position)] == EMPTY_TOKEN:

        if update_map:
            warehouse_map[tuple(next_position)] = warehouse_map[tuple(position)]
            warehouse_map[tuple(position)] = EMPTY_TOKEN

        return next_position

    # if move L/R, we can move as usual by considering each half as a box
    if (
        tuple(move) in [tuple(NPArray4Directions.LEFT), tuple(NPArray4Directions.RIGHT)]
        and warehouse_map[tuple(next_position)] in "[]"
    ):
        new_box_position = attempt_move_wider(warehouse_map, next_position, move)
        if new_box_position is not None:

            warehouse_map[tuple(next_position)] = warehouse_map[tuple(position)]
            warehouse_map[tuple(position)] = EMPTY_TOKEN

            return next_position

    elif tuple(move) in [tuple(NPArray4Directions.UP), tuple(NPArray4Directions.DOWN)]:

        boxes_left = np.argwhere(warehouse_map == "[")
        boxes_right = [tuple(box_left + (0, 1)) for box_left in boxes_left]
        boxes_left = [tuple(box_left) for box_left in boxes_left]

        encountered_box_id = None
        if tuple(next_position) in boxes_left:
            encountered_box_id = boxes_left.index(tuple(next_position))
        elif tuple(next_position) in boxes_right:
            encountered_box_id = boxes_right.index(tuple(next_position))

        if encountered_box_id is not None:
            if boxes_to_move is None:
                boxes_to_move = []
            next_left_position = attempt_move_wider(
                warehouse_map,
                boxes_left[encountered_box_id],
                move,
                False,
                boxes_to_move=boxes_to_move,
            )
            next_right_position = attempt_move_wider(
                warehouse_map,
                boxes_right[encountered_box_id],
                move,
                False,
                boxes_to_move=boxes_to_move,
            )

            boxes_to_move.append(encountered_box_id)

            if next_left_position is not None and next_right_position is not None:
                if update_map:
                    was_added = set()
                    for box_id in boxes_to_move:
                        if box_id not in was_added:
                            warehouse_map[tuple(move + boxes_left[box_id])] = "["
                            warehouse_map[tuple(move + boxes_right[box_id])] = "]"
                            warehouse_map[boxes_left[box_id]] = EMPTY_TOKEN
                            warehouse_map[boxes_right[box_id]] = EMPTY_TOKEN

                            was_added.add(box_id)

                    boxes_to_move = None

                    warehouse_map[tuple(next_position)] = warehouse_map[tuple(position)]
                    warehouse_map[tuple(position)] = EMPTY_TOKEN

                else:
                    boxes_to_move.append(encountered_box_id)

                return next_position


def resolve_moves(
    warehouse_map: np.ndarray,
    moves: list[np.ndarray],
    wider: bool = False,
    debug: bool = False,
) -> np.ndarray:
    move_fn = attempt_move if not wider else attempt_move_wider

    robot_starting_position = np.argwhere(warehouse_map == ROBOT_TOKEN)[-1]

    robot_position = robot_starting_position.copy()
    for move in moves:
        next_robot_position = move_fn(warehouse_map, robot_position, move)
        if next_robot_position is not None:
            robot_position = next_robot_position

        if debug:
            for row in warehouse_map:
                print("".join(c for c in row))
            input()
            os.system("clear")

    return warehouse_map


input_warehouse_map, input_robot_moves = read_input(raw_input=True).split("\n\n")

input_warehouse_map = np.array(list(map(list, input_warehouse_map.split("\n"))))
input_robot_moves = [
    DIRECTIONS_MAPPING[move] for move in input_robot_moves.replace("\n", "")
]

# part 1
warehouse_map = resolve_moves(input_warehouse_map.copy(), input_robot_moves)

boxes_positions = np.argwhere(warehouse_map == BOX_TOKEN)
gps_coordinates = [100 * coords[0] + coords[1] for coords in boxes_positions]
print(f"{sum(gps_coordinates)=}")

# part 2
np.set_printoptions(threshold=sys.maxsize)

modified_warehouse_map = np.empty(
    (input_warehouse_map.shape[0], input_warehouse_map.shape[1] * 2), dtype=str
)

for row_id, row in enumerate(input_warehouse_map):
    for col_id, val in enumerate(row):
        if val == WALL_TOKEN:
            wider_values = (WALL_TOKEN, WALL_TOKEN)
        if val == BOX_TOKEN:
            wider_values = ("[", "]")
        if val == EMPTY_TOKEN:
            wider_values = (EMPTY_TOKEN, EMPTY_TOKEN)
        if val == ROBOT_TOKEN:
            wider_values = (ROBOT_TOKEN, EMPTY_TOKEN)

        modified_warehouse_map[(row_id, col_id * 2)] = wider_values[0]
        modified_warehouse_map[(row_id, col_id * 2 + 1)] = wider_values[1]

solved_wider_warehouse_map = resolve_moves(
    modified_warehouse_map.copy(), input_robot_moves, wider=True
)

boxes_positions = np.argwhere(solved_wider_warehouse_map == "[")
gps_coordinates = [100 * coords[0] + coords[1] for coords in boxes_positions]
print(f"{sum(gps_coordinates)=}")
