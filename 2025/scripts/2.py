from typing import Optional
from aoc_utils import read_input


def parse_ids(ids_range_str: str) -> list[tuple[int, ...]]:
    ranges = ids_range_str.split(",")

    split_ranges = [tuple(map(int, range_str.split("-"))) for range_str in ranges]

    return split_ranges


def is_product_id_invalid(prod_id: int) -> bool:
    pattern_len = 1
    prod_id_str = str(prod_id)

    while pattern_len < len(prod_id_str):
        if (len(prod_id_str) % pattern_len) == 0:
            div_str = [
                prod_id_str[i : i + pattern_len]
                for i in range(0, len(prod_id_str), pattern_len)
            ]
            if all(s == div_str[0] for s in div_str):
                return True
        pattern_len += 1

    return False


input_ranges = read_input(as_type=parse_ids, one_line=True, separator=None)

invalid_ids = []

for id_range in input_ranges:
    start, end = id_range
    for prod_id in range(start, end + 1):
        if is_product_id_invalid(prod_id):
            invalid_ids.append(prod_id)

print(sum(invalid_ids))
