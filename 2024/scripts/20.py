from itertools import combinations
from typing import Optional
import numpy as np
from aoc_utils import read_input
from aoc_utils.enums.directions import NPArray4Directions

input_racetrack = read_input(as_type=list, to_numpy=True)

input_start_point = tuple(np.argwhere(input_racetrack == "S")[-1])
input_end_point = tuple(np.argwhere(input_racetrack == "E")[-1])


def dijkstra(
    racetrack: np.ndarray,
    start_point: tuple,
    end_point: tuple,
    cheating_allowed: bool = False,
) -> tuple[dict, Optional[list]]:
    if cheating_allowed:
        # third dimension to indicate if cheating or not
        start_point = (*start_point, 0)
        end_point = (*end_point, 0)

    dist_buffer = {start_point: 0}
    prev_buffer = {}
    graph_queue = [start_point]
    while graph_queue:
        extracted_point = min(graph_queue, key=lambda pt: dist_buffer[pt])
        graph_queue.remove(extracted_point)

        d = dist_buffer[extracted_point]

        if not cheating_allowed:
            neighbors = [
                tuple(direction + extracted_point)
                for direction in NPArray4Directions.to_list()
                if racetrack[tuple(direction + extracted_point)] != "#"
            ]
        else:
            if extracted_point[-1]:  # already cheated
                neighbors = [
                    (
                        direction[0] + extracted_point[0],
                        direction[1] + extracted_point[1],
                        1,
                    )
                    for direction in NPArray4Directions.to_list()
                    if all(
                        0 <= val < racetrack.shape[axis]
                        for axis, val in enumerate(
                            tuple(direction + extracted_point[:2])
                        )
                    )
                    and racetrack[tuple(direction + extracted_point[:2])] != "#"
                ]
            else:
                neighbors = [
                    (
                        direction[0] + extracted_point[0],
                        direction[1] + extracted_point[1],
                        int(racetrack[tuple(direction + extracted_point[:2])] == "#"),
                    )
                    for direction in NPArray4Directions.to_list()
                    if all(
                        0 <= val < racetrack.shape[axis]
                        for axis, val in enumerate(
                            tuple(direction + extracted_point[:2])
                        )
                    )
                ]

        for neighbor in neighbors:
            if neighbor not in dist_buffer or dist_buffer[neighbor] > d + 1:
                dist_buffer[neighbor] = d + 1
                graph_queue.append(neighbor)
                prev_buffer[neighbor] = extracted_point

    point = end_point
    path = [point]
    while start_point not in path:
        point = prev_buffer.get(point)
        if point is None:
            path = None
            break
        path.append(point)

    path = path[::-1] if path is not None else path

    return dist_buffer, path


# script
dist_buffer, path = dijkstra(
    racetrack=input_racetrack, start_point=input_start_point, end_point=input_end_point
)
baseline_race_time = dist_buffer[input_end_point]

# dist_buffer_from_start, path = dijkstra(
#     racetrack=input_racetrack, start_point=input_start_point, end_point=input_end_point,
#     cheating_allowed=True
# )

saved_times_base = []
saved_times_with_teleport = []
for first_point, second_point in combinations(dist_buffer.keys(), 2):
    manhattan_distance = abs(first_point[0] - second_point[0]) + abs(
        first_point[1] - second_point[1]
    )
    if manhattan_distance == 2:  # there can be a shortcut !
        saved_time = (
            dist_buffer[second_point] - dist_buffer[first_point] - manhattan_distance
        )
        saved_times_base.append(saved_time)
    if manhattan_distance <= 20:  # there can be a shortcut !
        saved_time = (
            dist_buffer[second_point] - dist_buffer[first_point] - manhattan_distance
        )
        saved_times_with_teleport.append(saved_time)

threshold = 100
print(len([time for time in saved_times_base if time >= threshold]))
print(len([time for time in saved_times_with_teleport if time >= threshold]))
