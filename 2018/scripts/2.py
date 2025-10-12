from aoc_utils import read_input
from collections import Counter
from itertools import product

input_box_ids = read_input()

n_twice, n_thrice = 0, 0

for box_id in input_box_ids:
    box_id_counter = Counter(box_id)
    n_twice += 2 in box_id_counter.values()
    n_thrice += 3 in box_id_counter.values()

print(n_thrice * n_twice)


def box_id_diff(first_box_id: str, second_box_id: str) -> int:
    n_diff = 0
    for c1, c2 in zip(first_box_id, second_box_id):
        if c1 != c2:
            n_diff += 1
    return n_diff


for box_id, other_box_id in product(input_box_ids, input_box_ids):
    n_diff = box_id_diff(box_id, other_box_id)
    if n_diff == 1:
        for c1, c2 in zip(box_id, other_box_id):
            if c1 == c2:
                print(c1, end="")
        print()
        break
