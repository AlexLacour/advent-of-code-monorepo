import numpy as np
from aoc_utils import read_input
from itertools import tee, zip_longest
import math

input_problems = read_input()

input_values_strs = input_problems[:-1]
input_operations_str = input_problems[-1]

operations_indices = [i for i, c in enumerate(input_operations_str) if c != " "]

split_input_values = []
for values_line in input_values_strs:
    start, end = tee(operations_indices)
    next(end)

    values = []
    for i, j in zip_longest(start, end):
        j = j - 1 if j is not None else j
        values.append(values_line[i:j])

    split_input_values.append(values)

input_values = np.asarray(split_input_values)
input_operations = input_operations_str.split()

first_total = 0
second_total = 0
for operation_id, operation_str in enumerate(input_operations):
    # let's cephalopod-solve this group
    group_of_numbers = input_values[:, operation_id]

    naive_read_numbers = map(int, group_of_numbers)
    first_res = (
        sum(naive_read_numbers)
        if operation_str == "+"
        else math.prod(naive_read_numbers)
    )
    first_total += first_res

    cephalopod_read_numbers = [
        int("".join([s[i] for s in group_of_numbers]))
        for i, _ in enumerate(group_of_numbers[0])
    ]
    second_res = (
        sum(cephalopod_read_numbers)
        if operation_str == "+"
        else math.prod(cephalopod_read_numbers)
    )
    second_total += second_res


print(first_total, second_total)
