from collections import defaultdict
from aoc_utils import read_input

input_frequencies = read_input(as_type=int)
print(sum(input_frequencies))

frequency = 0
frequencies_reached = {frequency}

f_index = 0
while True:
    f = input_frequencies[f_index % len(input_frequencies)]
    f_index += 1
    frequency += f
    if frequency not in frequencies_reached:
        frequencies_reached.add(frequency)
    else:
        print(frequency)
        break
