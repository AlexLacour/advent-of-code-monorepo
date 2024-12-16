from collections import defaultdict
import copy
from typing import Optional
import numpy as np
from aoc_utils import read_input
from aoc_utils.enums.directions import NPArray4Directions

input_maze = read_input(as_type=list, to_numpy=True)

# clockwise directions
DIRECTIONS_LIST = [
    NPArray4Directions.RIGHT,
    NPArray4Directions.DOWN,
    NPArray4Directions.LEFT,
    NPArray4Directions.UP,
]

start_tile = tuple(np.argwhere(input_maze == "S")[-1])
end_tile = tuple(np.argwhere(input_maze == "E")[-1])

# each move forward increases the score by 1
# each rotation (-90 or 90) increases the score by 1000 => rotate + move = score of 1001

# first solution : Dijkstra's algorithm ?
# buffers


def dijkstra(maze: np.ndarray, start: tuple, start_direction: int):
    dist_buffer = {}
    dist_buffer[(start, start_direction)] = 0

    prev_buffer = defaultdict(set)

    graph_queue = [(start, start_direction)]

    while graph_queue:
        extracted_point = min(graph_queue, key=lambda pt: dist_buffer[pt])
        graph_queue.remove(extracted_point)

        maze_position, maze_direction = extracted_point

        d = dist_buffer[extracted_point]

        for direction_id, _ in enumerate(DIRECTIONS_LIST):
            if direction_id != maze_direction:
                if (maze_position, direction_id) not in dist_buffer or dist_buffer[
                    (maze_position, direction_id)
                ] > d + 1000:
                    dist_buffer[(maze_position, direction_id)] = d + 1000
                    graph_queue.append((maze_position, direction_id))

        neighbor = tuple(DIRECTIONS_LIST[maze_direction] + maze_position)

        if maze[neighbor] != "#" and (
            (neighbor, maze_direction) not in dist_buffer
            or dist_buffer[(neighbor, maze_direction)] >= d + 1
        ):
            dist_buffer[(neighbor, maze_direction)] = d + 1
            graph_queue.append((neighbor, maze_direction))

            prev_buffer[(neighbor, maze_direction)].add((maze_position, maze_direction))

    return dist_buffer, prev_buffer


start_dist_buffer, _ = dijkstra(
    input_maze, start=start_tile, start_direction=0
)
pos_dir, lowest_cost = min(
    [
        (coord_dir, val)
        for coord_dir, val in start_dist_buffer.items()
        if coord_dir[0] == end_tile
    ],
    key=lambda x: x[1],
)
print(f"{lowest_cost=}")

pos, dir = pos_dir
flip_dir = (dir + 2) % 4
end_dist_buffer, _ = dijkstra(
    input_maze, start=end_tile, start_direction=flip_dir
)

good_seats = set()
for point in np.argwhere(input_maze != "#"):
    point = tuple(point)
    for direction_id, _ in enumerate(DIRECTIONS_LIST):
        if (
            start_dist_buffer[(point, direction_id)]
            + end_dist_buffer[(point, (direction_id + 2) % 4)]
            == lowest_cost
        ):
            good_seats.add(point)

print(f"{len(good_seats)=}")
