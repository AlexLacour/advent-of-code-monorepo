import math
import re
from collections import Counter
from itertools import combinations

from aoc_utils import read_input


def parse_line(record_line_str: str) -> tuple[str, list]:
    springs_states, contiguous_groups_len = record_line_str.split()
    contiguous_groups_len_list = list(map(int, contiguous_groups_len.split(",")))
    return springs_states, contiguous_groups_len_list


input_condition_records = read_input(as_type=parse_line)


def is_states_valid(states_str: str, contiguous_lens: list[int]) -> bool:
    base_regex = ""
    for val_id, value in enumerate(contiguous_lens):
        if val_id:
            base_regex += r"\.+"
        base_regex += r"\#{{{}}}".format(value)

    matches = list(re.findall(base_regex, states_str))
    if matches:
        return True
    return False


def get_number_of_arrangements(condition_record: tuple[str, list]) -> int:
    springs_states, contiguous_damaged_lens = condition_record

    number_of_damaged_to_put = (
        sum(contiguous_damaged_lens) - Counter(springs_states)["#"]
    )

    unknown_points = [match.start() for match in re.finditer("\?", springs_states)]

    n_arrangements = 0
    for combination in combinations(unknown_points, number_of_damaged_to_put):
        springs_states_list = list(springs_states)
        for i in unknown_points:
            springs_states_list[i] = "#" if i in combination else "."

        if is_states_valid("".join(springs_states_list), contiguous_damaged_lens):
            n_arrangements += 1
    return n_arrangements


print(
    "P1",
    sum(
        get_number_of_arrangements(condition_record)
        for condition_record in input_condition_records
    ),
)
