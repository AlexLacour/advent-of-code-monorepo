from queue import Queue

import numpy as np

from aoc_utils import read_input

RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)


input_heat_grid = read_input(as_type=lambda x: list(map(int, x)), to_numpy=True)

def min_cost_path(heat_grid: np.ndarray, source: tuple, destination: tuple):
    tc = np.zeros(heat_grid.shape)
    tc[source] = heat_grid[source]

    m, n = destination

    for i in range(1, m+1):
        tc[i][0] = tc[i-1][0] + heat_grid[i][0]
 
    # Initialize first row of tc array
    for j in range(1, n+1):
        tc[0][j] = tc[0][j-1] + heat_grid[0][j]
 
    # Construct rest of the tc array
    for i in range(1, m+1):
        for j in range(1, n+1):
            tc[i][j] = min(tc[i-1][j-1], tc[i-1][j], tc[i][j-1]) + heat_grid[i][j]
    return tc


res = min_cost_path(input_heat_grid, (0, 0))
print(res)