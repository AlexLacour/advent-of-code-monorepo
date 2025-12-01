from typing import Sequence
from aoc_utils import read_input


def parse_rotation(rotation_str) -> int:
    return (
        int(rotation_str[1:]) if rotation_str[0] == "R" else int(rotation_str[1:]) * -1
    )


input_rotation_sequence = read_input(as_type=parse_rotation)

dial = list(range(100))

first_dial_value = 50

rotation_index = dial.index(first_dial_value)

first_password = 0
password = 0

for turn in input_rotation_sequence:
    tmp_rotation_index = rotation_index + turn

    # P1
    if tmp_rotation_index == 0:
        password += 1
    elif tmp_rotation_index > 99:
        password += tmp_rotation_index // 100
    elif tmp_rotation_index < 0:
        password += abs(tmp_rotation_index) // 100
        if rotation_index != 0:
            password += 1

    rotation_index = tmp_rotation_index % 100
    if rotation_index == 0:
        first_password += 1


print(first_password, password)
