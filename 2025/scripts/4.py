import numpy as np
from aoc_utils import read_input
from aoc_utils.enums.directions import NPArray8Directions

input_grid: np.ndarray = read_input(as_type=list, to_numpy=True)  # type: ignore

# replace grid to num
input_grid[input_grid == "@"] = 1
input_grid[input_grid == "."] = 0
input_grid = input_grid.astype(int)

# padding
padded_grid = np.pad(input_grid, pad_width=1)
# script


def get_movable_rolls(paper_rolls_grid: np.ndarray) -> list[tuple]:
    paper_rolls_positions = np.argwhere(paper_rolls_grid > 0)

    movable_rolls = []
    for paper_roll_pos in paper_rolls_positions:
        neighbor_positions = [
            tuple(npos + paper_roll_pos) for npos in NPArray8Directions.to_list()
        ]
        n_pos_row = [n[0] for n in neighbor_positions]
        n_pos_col = [n[1] for n in neighbor_positions]

        n_adjacent_rolls = sum(paper_rolls_grid[n_pos_row, n_pos_col])

        # movable
        if n_adjacent_rolls < 4:
            movable_rolls.append(paper_roll_pos)

    return movable_rolls


total_removed_rolls_hist = []
while True:
    movable_rolls = get_movable_rolls(padded_grid)
    if not movable_rolls:
        break
    total_removed_rolls_hist.append(len(movable_rolls))

    removed_row = [r[0] for r in movable_rolls]
    removed_col = [r[1] for r in movable_rolls]

    padded_grid[removed_row, removed_col] = 0

print(total_removed_rolls_hist[0], sum(total_removed_rolls_hist))
