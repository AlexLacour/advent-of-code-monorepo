import numpy as np

from aoc_utils import read_input

input_presents = [
    item.split("\n") for item in read_input(raw_input=True).split("\n\n")
]

presents = [
    np.asarray([list(line) for line in present_lines[1:]], dtype=str)
    for present_lines in input_presents[:-1]
]
regions_requirements_strs = [
    size_and_reqs.split(": ") for size_and_reqs in input_presents[-1]
]
regions_requirements = [
    (tuple(map(int, size.split("x"))), list(map(int, reqs.split())))
    for size, reqs in regions_requirements_strs
]
