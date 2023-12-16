from typing import Optional

import numpy as np

from aoc_utils import read_input

input_tiles = read_input(as_type=list, to_numpy=True)

RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)

DIRECTION_UPDATES = {
    "/": {
        RIGHT: UP,  # right to up
        DOWN: LEFT,  # down to left
        LEFT: DOWN,  # left to down
        UP: RIGHT,  # up to right
    },
    "\\": {
        RIGHT: DOWN,  # right to down
        DOWN: RIGHT,  # down to right
        LEFT: UP,  # left to up
        UP: LEFT,  # up to left
    },
}


ENERGY_MAP_CACHE = {}


def move_beam(
    tiles: np.ndarray,
    beam_starting_position: tuple,
    beam_starting_direction: tuple,
    energy_map: Optional[np.ndarray] = None,
    started_beams: Optional[set] = None,
) -> np.ndarray:
    # init data structures
    if energy_map is None:
        energy_map = np.zeros(tiles.shape)
    map_height, map_width = energy_map.shape

    if started_beams is None:
        started_beams = set()

    beam_position = beam_starting_position
    beam_direction = beam_starting_direction
    started_beams.add(beam_position)
    # run beam
    while True:
        # update direction
        if input_tiles[beam_position] in ["/", "\\"]:
            beam_direction = DIRECTION_UPDATES[input_tiles[beam_position]][
                beam_direction
            ]

        # potential split
        elif input_tiles[beam_position] == "-" and beam_direction in [UP, DOWN]:
            if beam_position not in started_beams:
                energy_map = move_beam(
                    tiles, beam_position, LEFT, energy_map, started_beams
                )
                energy_map = move_beam(
                    tiles, beam_position, RIGHT, energy_map, started_beams
                )
            break

        elif input_tiles[beam_position] == "|" and beam_direction in [LEFT, RIGHT]:
            if beam_position not in started_beams:
                energy_map = move_beam(
                    tiles, beam_position, UP, energy_map, started_beams
                )
                energy_map = move_beam(
                    tiles, beam_position, DOWN, energy_map, started_beams
                )
            break

        # energy tracking
        energy_map[beam_position] += 1

        # position update
        beam_position = tuple(np.array(beam_position) + beam_direction)

        # out of map => end
        if not (
            0 <= beam_position[0] < map_height and 0 <= beam_position[1] < map_width
        ):
            break

    ENERGY_MAP_CACHE[(beam_starting_position, beam_starting_direction)] = energy_map
    return energy_map


def get_number_of_energized_tiles(energy_map: np.ndarray) -> int:
    return len(np.where(energy_map > 0)[0])


def get_candidates(tiles: np.ndarray) -> list[tuple]:
    height, width = tiles.shape
    downwards = [((0, i), DOWN) for i in range(width)]
    upwards = [((height - 1, i), UP) for i in range(width)]
    lefts = [((i, width - 1), LEFT) for i in range(height)]
    rights = [((i, 0), RIGHT) for i in range(height)]
    return [*downwards, *upwards, *lefts, *rights]


# P1
print(
    "P1",
    get_number_of_energized_tiles(
        move_beam(
            tiles=input_tiles,
            beam_starting_position=(0, 0),
            beam_starting_direction=RIGHT,
        )
    ),
)


# P2
print(
    "P2",
    max(
        get_number_of_energized_tiles(
            ENERGY_MAP_CACHE[candidate]
            if candidate in ENERGY_MAP_CACHE
            else move_beam(input_tiles, *candidate)
        )
        for candidate in get_candidates(input_tiles)
    ),
)
