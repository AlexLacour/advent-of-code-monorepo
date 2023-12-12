import math
import re
from collections import Counter

from aoc_utils import read_input


def parse_line(record_line_str: str) -> tuple[str, list]:
    springs_states, contiguous_groups_len = record_line_str.split()
    contiguous_groups_len_list = list(map(int, contiguous_groups_len.split(",")))
    return springs_states, contiguous_groups_len_list


input_condition_records = read_input(as_type=parse_line)

for condition_record in input_condition_records:
    springs_states, contiguous_damaged_lens = condition_record
    
    number_of_damaged_to_put = sum(contiguous_damaged_lens) - Counter(springs_states)["#"]

    number_of_unknown_points = len([match.start() for match in re.finditer("\?", springs_states)])

    # number of sure cases
    number_of_sure_points = 0
    number_of_associated_damaged = 0

    for contiguous_damaged_len in contiguous_damaged_lens:
        matches = list(re.finditer(r"[\?\#]{{{}}}".format(contiguous_damaged_len), springs_states))
        print([match.group() for match in matches])

    number_of_ambivalent_points = number_of_unknown_points - number_of_sure_points
    number_of_damaged_remaining_to_put = number_of_damaged_to_put - number_of_associated_damaged
    n_arrangements = math.comb(number_of_ambivalent_points, number_of_damaged_remaining_to_put)

    print(n_arrangements)
