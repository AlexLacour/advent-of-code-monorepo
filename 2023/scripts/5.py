from aoc_utils import read_input


def parse_almanac_data(almanac_data_str: str) -> dict:
    almanac_data = almanac_data_str.split("\n\n")
    seeds = list(map(int, almanac_data[0].split(":")[-1].split()))

    raw_maps = almanac_data[1:]

    clean_maps = {}
    for new_map in raw_maps:
        map_name, map_raw_content = new_map.split(":")

        map_ranges = [list(map(int, map_range.split())) for map_range in map_raw_content.split("\n") if map_range]

        clean_maps[map_name] = map_ranges

    return {"seeds": seeds, "maps": clean_maps}


input_almanac_data = parse_almanac_data(read_input(raw_input=True))


def apply_all_maps_to_value(value: int, series_of_maps: list) -> int:
    for component_maps in series_of_maps:
        for component_map in component_maps:
            dst_start, src_start, length = component_map

            if value in range(src_start, src_start + length):
                value = dst_start + (value - src_start)
                break
    return value


def get_min_location(almanac_data: dict) -> int:
    min_location = None
    for seed in almanac_data["seeds"]:
        value_to_transform = apply_all_maps_to_value(seed, almanac_data["maps"].values())
        
        if min_location is None or value_to_transform < min_location:
            min_location = value_to_transform
    return min_location


def part2(almanac_data: dict):
    seed_ranges = list(zip(*[iter(almanac_data["seeds"])] * 2))
    print(seed_ranges)



print("P1", get_min_location(input_almanac_data))
print("P2", part2(input_almanac_data))