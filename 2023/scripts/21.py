import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

from aoc_utils import read_input

RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)
DIRECTIONS = {"R": RIGHT, "L": LEFT, "U": UP, "D": DOWN}


input_garden = read_input(as_type=list, to_numpy=True)

starting_position = [(x, y) for x, y in zip(*np.where(input_garden == "S"))][0]
print("S", starting_position)
possible_visited_tiles = {}
n_steps = 64
positions = [starting_position]
h, w = input_garden.shape
for step_id in tqdm(range(n_steps)):
    candidates = set(
        [
            tuple(np.array(direction) + position)
            for direction in DIRECTIONS.values()
            for position in positions
        ]
    )

    positions = [
        candidate
        for candidate in candidates
        if 0 <= candidate[0] < h
        and 0 <= candidate[1] < w
        and input_garden[candidate] != "#"
    ]

    possible_visited_tiles[step_id + 1] = positions

    busy_spots = [
        candidate
        for candidate in candidates
        if 0 <= candidate[0] < h
        and 0 <= candidate[1] < w
        and input_garden[candidate] == "#"
    ]
    print(step_id + 1, len(busy_spots))

    # display_map = np.zeros(input_garden.shape)
    # for point in positions:
    #     display_map[point] = 1
    # plt.imshow(display_map)
    # plt.show()    

print("P1", len(possible_visited_tiles[n_steps]))
