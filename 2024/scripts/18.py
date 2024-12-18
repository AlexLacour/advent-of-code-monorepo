from typing import Optional
from aoc_utils import read_input
import numpy as np
from aoc_utils.enums.directions import NPArray4Directions

input_memory_coordinates: list[tuple[int, int]] = read_input(
    as_type=lambda line: tuple(map(int, line.split(",")))
)

# dijkstra


def dijkstra(
    memory_map: np.ndarray, start_point: tuple, exit_point: tuple
) -> tuple[dict, Optional[list]]:
    dist_buffer = {start_point: 0}
    prev_buffer = {}
    graph_queue = [start_point]
    while graph_queue:
        extracted_point = min(graph_queue, key=lambda pt: dist_buffer[pt])
        graph_queue.remove(extracted_point)

        d = dist_buffer[extracted_point]

        neighbors = [
            tuple(direction + extracted_point)
            for direction in NPArray4Directions.to_list()
            if all(
                0 <= val < memory_map.shape[axis]
                for axis, val in enumerate(tuple(direction + extracted_point))
            )
            and memory_map[tuple(direction + extracted_point)] == 0
        ]

        for neighbor in neighbors:
            if neighbor not in dist_buffer or dist_buffer[neighbor] > d + 1:
                dist_buffer[neighbor] = d + 1
                graph_queue.append(neighbor)
                prev_buffer[neighbor] = extracted_point

    point = exit_point
    path = [point]
    while start_point not in path:
        point = prev_buffer.get(point)
        if point is None:
            path = None
            break
        path.append(point)

    path = path[::-1] if path is not None else path

    return dist_buffer, path


grid_range = 70
memory_map = np.zeros((grid_range + 1, grid_range + 1))

fallen_bytes = 1024
for coord in input_memory_coordinates[:fallen_bytes]:
    np_coord = coord[::-1]
    memory_map[np_coord] += 1

start = (0, 0)
exit_point = (grid_range, grid_range)

dist_buffer, path = dijkstra(memory_map, start, exit_point)

print(f"{dist_buffer[exit_point]=}")

for coord in input_memory_coordinates[fallen_bytes:]:
    np_coord = coord[::-1]

    memory_map[np_coord] += 1

    if np_coord in path:
        dist_buffer, path = dijkstra(memory_map, start, exit_point)
        if path is None:
            coord_str = ",".join(map(str, coord))
            print(f"{coord_str=}")
            break
