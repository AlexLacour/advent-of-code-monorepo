import re

from aoc_utils import read_input

calibration_values = read_input()


str_to_int = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def extract_number_from_value(
    value: str, contains_spelled_numbers: bool = False
) -> int:
    number_dict = {}

    if contains_spelled_numbers:
        for int_equivalent, str_value in enumerate(str_to_int):
            found_indexes = [match.start() for match in re.finditer(str_value, value)]
            for found_index in found_indexes:
                number_dict[found_index] = str(int_equivalent + 1)

    for c_index, c in enumerate(value):
        if c.isdigit():
            number_dict[c_index] = c

    number_dict = dict(sorted(number_dict.items()))

    number_list = list(number_dict.values())

    numbers_to_keep = [number_list[0], number_list[-1]]
    return int("".join(numbers_to_keep))


print("P1", sum([extract_number_from_value(val) for val in calibration_values]))
print(
    "P2",
    sum(
        [
            extract_number_from_value(val, contains_spelled_numbers=True)
            for val in calibration_values
        ]
    ),
)
