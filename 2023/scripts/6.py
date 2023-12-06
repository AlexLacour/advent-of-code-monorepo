import math

from aoc_utils import read_input


def parse_line(line_str: str) -> list:
    return list(map(int, line_str.split(":")[-1].split()))


input_times, input_distances_records = read_input(as_type=parse_line)


def beat_race(race_time: int, race_distance_record: int) -> list[int]:
    record_beating_times = []
    for n_ms_pressed in range(race_time + 1):
        speed = n_ms_pressed

        distance = (race_time - n_ms_pressed) * speed

        if distance > race_distance_record:
            record_beating_times.append(n_ms_pressed)

    return record_beating_times


def get_n_ways_to_beat_races(times: list, dist_records: list) -> list[int]:
    return [len(beat_race(time, dist)) for time, dist in zip(times, dist_records)]


print("P1", math.prod(get_n_ways_to_beat_races(input_times, input_distances_records)))

combined_input_time = int("".join(map(str, input_times)))
combined_input_distance_record = int("".join(map(str, input_distances_records)))
print("P2", len(beat_race(combined_input_time, combined_input_distance_record)))
