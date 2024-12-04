import copy
import numpy as np
from aoc_utils import read_input
from aoc_utils.enums.directions import NPArray8Directions
from collections import Counter, defaultdict
from itertools import combinations


PUZZLE_LETTERS = ".XMAS"


def check_next_value(
    grid: np.ndarray, position: np.ndarray, direction: np.ndarray
) -> bool:
    candidate = position + direction
    # bounds condition
    if any(val < 0 or val >= grid.shape[dim] for dim, val in enumerate(candidate)):
        return False

    elif grid[tuple(candidate)] == (grid[tuple(position)] + 1):
        # then we can search for the rest of the word
        return True

    else:
        return False


def find_words(grid: np.ndarray, pattern: str) -> set:
    found_words = set()
    for position in np.argwhere(grid == PUZZLE_LETTERS.index(pattern[0])):
        # find the next letter around
        for direction in NPArray8Directions.to_list():
            potential_word_position = copy.deepcopy(position)
            for _ in enumerate(pattern):
                if PUZZLE_LETTERS[grid[tuple(potential_word_position)]] == pattern[-1]:
                    found_words.add((tuple(position), tuple(direction)))

                if not check_next_value(
                    grid=grid,
                    position=potential_word_position,
                    direction=direction,
                ):
                    break
                potential_word_position = potential_word_position + direction
    return found_words


input_word_search = read_input(
    as_type=lambda line: [PUZZLE_LETTERS.index(c) for c in line], to_numpy=True
)

found_xmas = find_words(grid=input_word_search, pattern="XMAS")
print(f"{len(found_xmas)=}")

# Part 2
found_mas = find_words(grid=input_word_search, pattern="MAS")

allowed_x_directions = [
    tuple(NPArray8Directions.UPRIGHT),
    tuple(NPArray8Directions.DOWNRIGHT),
    tuple(NPArray8Directions.UPLEFT),
    tuple(NPArray8Directions.DOWNLEFT),
]

a_positions_with_directions = [
    (tuple(np.array(found[0]) + np.array(found[1])), found[1])
    for found in found_mas
    if tuple(found[1]) in allowed_x_directions
]

directions_by_position = defaultdict(list)
for a_position, direction in a_positions_with_directions:
    directions_by_position[a_position].append(direction)

x_number = 0
for directions in directions_by_position.values():
    if len(directions) <= 1:
        continue
    inner_products = [np.inner(*vec_pair) for vec_pair in combinations(directions, 2)]
    x_number += Counter(inner_products).get(0, 0)

print(f"{x_number=}")
