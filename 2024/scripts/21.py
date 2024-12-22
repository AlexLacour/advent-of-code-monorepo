import copy
from aoc_utils import read_input
import numpy as np

input_keypad_codes = read_input()

NUMERIC_KEYPAD = np.asarray(
    [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", "A"]]
)
DIRECTIONAL_KEYPAD = np.asarray([[None, "^", "A"], ["<", "v", ">"]])

KEYPADS = {"numeric": NUMERIC_KEYPAD, "directional": DIRECTIONAL_KEYPAD}


def get_moves_to_target(
    target: int | str, position: tuple, keypad_type: str
) -> list[str]:
    keypad = KEYPADS[keypad_type]
    target_position = tuple(np.argwhere(keypad == target)[-1])

    moves = []

    x_distance = target_position[1] - position[1]
    y_distance = target_position[0] - position[0]

    if not x_distance or not y_distance:
        for _ in range(abs(x_distance)):
            moves.append(">" if x_distance > 0 else "<")
        for _ in range(abs(y_distance)):
            moves.append("v" if y_distance > 0 else "^")
    elif keypad[(position[0], position[1] + x_distance)] is None:
        for _ in range(abs(y_distance)):
            moves.append("v" if y_distance > 0 else "^")
        for _ in range(abs(x_distance)):
            moves.append(">" if x_distance > 0 else "<")
    elif keypad[(position[0] + y_distance, position[1])] is None:
        for _ in range(abs(x_distance)):
            moves.append(">" if x_distance > 0 else "<")
        for _ in range(abs(y_distance)):
            moves.append("v" if y_distance > 0 else "^")
    else:
        for _ in range(abs(x_distance)):
            moves.append(">" if x_distance > 0 else "<")
        for _ in range(abs(y_distance)):
            moves.append("v" if y_distance > 0 else "^")
        moves.sort(key="<v^>".index)  # sort by approximative distance to the "A" button

    return moves


# script
# setup
num_direction_robots = 2
direction_robots_positions = [
    tuple(np.argwhere(DIRECTIONAL_KEYPAD == "A")[0])
    for _ in range(num_direction_robots)
]
numeric_robot_position = tuple(np.argwhere(NUMERIC_KEYPAD == "A")[0])

complexities = []

for code in input_keypad_codes:
    # code_moves = []
    code_moves_len = 0
    for target in code:
        pressed_keys = get_moves_to_target(
            target, numeric_robot_position, keypad_type="numeric"
        )
        if pressed_keys:
            numeric_robot_position = tuple(np.argwhere(NUMERIC_KEYPAD == target)[0])
        pressed_keys.append("A")

        for robot_id in range(num_direction_robots):
            new_pressed_keys = []
            for target in pressed_keys:
                keys_needed_to_move = get_moves_to_target(
                    target,
                    direction_robots_positions[robot_id],
                    keypad_type="directional",
                )

                if keys_needed_to_move:
                    direction_robots_positions[robot_id] = tuple(
                        np.argwhere(DIRECTIONAL_KEYPAD == target)[0]
                    )
                keys_needed_to_move.append("A")

                new_pressed_keys.extend(keys_needed_to_move)
            pressed_keys = new_pressed_keys

        code_moves_len += len(pressed_keys)
        # code_moves.extend(pressed_keys)
    # print(int(code.replace("A", "")), len(code_moves), "".join(code_moves))
    complexities.append(int(code.replace("A", "")) * code_moves_len)

print(f"{sum(complexities)=}")
