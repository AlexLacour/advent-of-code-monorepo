import copy

from aoc_utils import read_input


def parse_almanac_data(almanac_data_str: str) -> dict:
    almanac_data = almanac_data_str.split("\n\n")
    seeds = list(map(int, almanac_data[0].split(":")[-1].split()))

    raw_maps = almanac_data[1:]

    clean_maps = {}
    for new_map in raw_maps:
        map_name, map_raw_content = new_map.split(":")

        map_ranges = [
            list(map(int, map_range.split()))
            for map_range in map_raw_content.split("\n")
            if map_range
        ]

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


def get_min_location_with_single_seed(almanac_data: dict) -> int:
    min_location = None
    for seed in almanac_data["seeds"]:
        value_to_transform = apply_all_maps_to_value(
            seed, almanac_data["maps"].values()
        )

        if min_location is None or value_to_transform < min_location:
            min_location = value_to_transform
    return min_location


def apply_component_maps_to_range(
    range_to_udpate: tuple, component_maps: list
) -> list[tuple]:
    value_start, value_length = range_to_udpate
    _value_end = value_start + value_length

    for map_id, component_map in enumerate(component_maps):
        dst_start, src_start, length = component_map
        _src_end = src_start + length

        transformation = dst_start - src_start

        # no split, all transform
        if src_start <= value_start and _value_end <= _src_end:  # case 1
            return [(value_start + transformation, value_length)]

        # split in 2
        elif value_start < src_start and (src_start < _value_end <= _src_end):  # case 2
            out_tuple = (value_start, src_start - value_start)
            in_tuple = (dst_start, _value_end - src_start)
            return [
                *apply_component_maps_to_range(out_tuple, component_maps[map_id + 1 :]),
                in_tuple,
            ]

        # split in 2
        elif src_start <= value_start < _src_end and _src_end < _value_end:  # case 2b
            in_tuple = (dst_start + value_start - src_start, _src_end - value_start)
            out_tuple = (_src_end, _value_end - _src_end)

            return [
                *apply_component_maps_to_range(out_tuple, component_maps[map_id + 1 :]),
                in_tuple,
            ]

        # split in 3
        elif value_start <= src_start and _src_end <= _value_end:  # case 3
            left_tuple = (value_start, src_start - value_start)
            mid_tuple = (dst_start, length)
            right_tuple = (_src_end, _value_end - _src_end)
            return [
                *apply_component_maps_to_range(
                    left_tuple, component_maps[map_id + 1 :]
                ),
                mid_tuple,
                *apply_component_maps_to_range(
                    right_tuple, component_maps[map_id + 1 :]
                ),
            ]

    return [range_to_udpate]


def get_min_location_with_seed_range(almanac_data: dict):
    seed_ranges = list(zip(*[iter(almanac_data["seeds"])] * 2))

    updated_ranges = copy.deepcopy(seed_ranges)

    for component_maps in almanac_data["maps"].values():
        new_updated_ranges = []

        for range_to_update in updated_ranges:
            new_updated_ranges.extend(
                apply_component_maps_to_range(range_to_update, component_maps)
            )

        updated_ranges = copy.deepcopy(new_updated_ranges)

    return min(updated_ranges, key=lambda x: x[0])[0]


print("P1", get_min_location_with_single_seed(input_almanac_data))
print("P2", get_min_location_with_seed_range(input_almanac_data))
