from queue import Queue

import numpy as np

from aoc_utils import read_input

RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)


input_heat_grid = read_input(as_type=lambda x: list(map(int, x)), to_numpy=True)

def run_dijkstra(heat_grid: np.ndarray, source: tuple[int, int]):
    unvisited = {(line_id, col_id) for line_id, line in enumerate(heat_grid) for col_id, _ in enumerate(line)}
    distances = {point: np.inf for point in unvisited}
    distances[source] = heat_grid[source]
    prev = {}

    while unvisited:
        current_node = min(list(unvisited), key=distances.get)

        neighbors = [tuple(np.asarray(current_node) + direction) for direction in [LEFT, RIGHT, UP, DOWN]]
        neighbors = [n for n in neighbors if n in unvisited]

        for neighbor_point in neighbors:
            if (alt := distances[current_node] + heat_grid[neighbor_point]) < distances[neighbor_point]:
                distances[neighbor_point] = alt
                prev[neighbor_point] = current_node

        unvisited.remove(current_node)

    # to numpy
    distances_np = np.zeros(heat_grid.shape)
    for point, distance in distances.items():
        distances_np[point] = distance
    return distances_np, prev


res, paths = run_dijkstra(input_heat_grid, (0, 0))
print(res)