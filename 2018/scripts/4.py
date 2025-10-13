from collections import defaultdict
from typing import Optional

import numpy as np
from aoc_utils import read_input
from datetime import datetime


def _parse_line(line_str: str) -> Optional[tuple[datetime, str]]:
    event_datetime, event_str = line_str.split("]")
    event_datetime = datetime.strptime(event_datetime[1:], "%Y-%m-%d %H:%M")

    if "#" in event_str:
        return event_datetime, event_str.split()[1]
    elif "asleep" in event_str:
        return event_datetime, "1"
    elif "up" in event_str:
        return event_datetime, "0"


input_events = read_input(as_type=_parse_line)
input_events: list[tuple[datetime, str]] = sorted(input_events, key=lambda x: x[0])

full_shift_historic = defaultdict(list)

current_guard = None
asleep = False
asleep_time = None
shift_data = np.zeros((60,))

for event_date, event in input_events:
    if "#" in event:
        if current_guard is not None:
            full_shift_historic[current_guard].append(shift_data)
        current_guard = event
        shift_data = np.zeros((60,))
    elif event == "1":
        asleep = True
        asleep_time = event_date.minute
    elif event == "0":
        asleep = False
        shift_data[asleep_time:event_date.minute] = 1
else:
    full_shift_historic[current_guard].append(shift_data)


most_sleepy_guard = max(full_shift_historic, key=lambda x: np.sum(full_shift_historic[x]))
best_minute = int(np.argmax(np.sum(full_shift_historic[most_sleepy_guard], axis=0)))

res = int(most_sleepy_guard[1:]) * best_minute
print(res)

most_frequent_guard = max(full_shift_historic, key=lambda x: max(np.sum(full_shift_historic[x], axis=0)))
best_minute = int(np.argmax(np.sum(full_shift_historic[most_frequent_guard], axis=0)))

res = int(most_frequent_guard[1:]) * best_minute
print(res)
