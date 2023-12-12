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

    mandatory_functional_indexes = set()
    for contiguous_damaged_len in contiguous_damaged_lens:
        candidates = list(
            re.finditer(
                r"(?<=\?)\#{" + str(contiguous_damaged_len) + r"}(?=\?|$|\.)", springs_states
            )
        )
        if candidates:
            damaged_span = candidates[0].span()
            if damaged_span[0] - 1 >= 0:
                mandatory_functional_indexes.add(damaged_span[0] - 1)
            if damaged_span[-1] <= len(springs_states):
                mandatory_functional_indexes.add(damaged_span[-1])
    
    print(springs_states, mandatory_functional_indexes)

    unknown_ids = {match.start(): True for match in re.finditer("\?", springs_states)}

    unknown_and_damaged_groups = [group for group in springs_states.split(".") if group]
    number_of_splits_to_create = len(contiguous_damaged_lens) - len(
        unknown_and_damaged_groups
    )

    initial_states_counter = Counter(springs_states)
    number_of_damaged_to_put = (
        sum(contiguous_damaged_lens) - initial_states_counter["#"]
    )

    # Final computation
    n_arrangements = math.comb(
        len(unknown_ids) - (number_of_splits_to_create + len(mandatory_functional_indexes)), number_of_damaged_to_put
    )
    print(n_arrangements)
