from aoc_utils import read_input
from collections import Counter

input_location_ids: list[tuple[int, int]] = read_input(
    as_type=lambda line: tuple(map(int, line.split()))
)

first_group_location_ids, second_group_location_ids = list(zip(*input_location_ids))

# Part 1
location_distances_list = [
    abs(first_location - second_location)
    for first_location, second_location in zip(
        sorted(first_group_location_ids), sorted(second_group_location_ids)
    )
]
print(f"{sum(location_distances_list)=}")

# Part 2
second_group_counter = Counter(second_group_location_ids)

sim_score = 0

for location_id in first_group_location_ids:
    sim_score += location_id * second_group_counter.get(location_id, 0)

print(f"{sim_score=}")
