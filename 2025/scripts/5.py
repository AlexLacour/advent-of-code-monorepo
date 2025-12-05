from aoc_utils import read_input

fresh_id_ranges__ingredient_ids: list[str] = read_input(raw_input=True).split("\n\n")
# parsing
tmp_fresh_id_ranges: list[str] = fresh_id_ranges__ingredient_ids[0].split("\n")
tmp_ingredient_ids: list[str] = fresh_id_ranges__ingredient_ids[1].split("\n")

# casting
fresh_id_ranges: list[tuple[int, ...]] = [
    tuple(map(int, r.split("-"))) for r in tmp_fresh_id_ranges
]
ingredient_ids: set[int] = set([int(i) for i in tmp_ingredient_ids])

# script
fresh_counter = 0
for ingredient_id in ingredient_ids:
    for range_min, range_max in fresh_id_ranges:
        if range_min <= ingredient_id <= range_max:
            fresh_counter += 1
            break

print(fresh_counter)

sorted_fresh_id_ranges = sorted(fresh_id_ranges, key=lambda x: x[0])
clamped_fresh_id_ranges = []

range_id = 0
neighbor_step = 1
while range_id < len(sorted_fresh_id_ranges):
    go_to_next_range = False

    if sorted_fresh_id_ranges[range_id] == (-1, -1):
        range_id += 1
        continue

    range_min, range_max = sorted_fresh_id_ranges[range_id]
    new_range_min = range_min
    new_range_max = range_max

    neighbor = range_id + neighbor_step

    if (
        range_id < len(sorted_fresh_id_ranges) - neighbor_step
        and range_max >= sorted_fresh_id_ranges[neighbor][0]
    ):
        if range_max < sorted_fresh_id_ranges[neighbor][1]:  # simple overlap, we shift
            new_range_max = sorted_fresh_id_ranges[neighbor][0] - 1

            go_to_next_range = True
        else:  # inclusion, we absorb by 'erasing' the neighbor, and we check the next neighbor
            sorted_fresh_id_ranges[neighbor] = (-1, -1)
            neighbor_step += 1
    else:
        go_to_next_range = True

    if go_to_next_range:
        range_id += 1
        neighbor_step = 1

        clamped_fresh_id_ranges.append([new_range_min, new_range_max])

range_total = sum([r_max - r_min + 1 for r_min, r_max in clamped_fresh_id_ranges])
print(range_total)
