from enum import Enum

import numpy as np


class BasicDirections(Enum):
    UP = (1, 0)
    DOWN = (-1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class NPBasicDirections:
    UP = np.array(BasicDirections.UP)
    DOWN = np.array(BasicDirections.DOWN)
    LEFT = np.array(BasicDirections.LEFT)
    RIGHT = np.array(BasicDirections.RIGHT)


class NPArray4Directions:
    UP = np.array((-1, 0))
    DOWN = np.array((1, 0))
    LEFT = np.array((0, -1))
    RIGHT = np.array((0, 1))


class NPArray8Directions:
    UP = np.array((-1, 0))
    DOWN = np.array((1, 0))
    LEFT = np.array((0, -1))
    RIGHT = np.array((0, 1))
    UPRIGHT = np.array((-1, 1))
    DOWNRIGHT = np.array((1, 1))
    UPLEFT = np.array((-1, -1))
    DOWNLEFT = np.array((1, -1))
    
    def to_list() -> list[np.ndarray]:
        return [
            NPArray8Directions.UP,
            NPArray8Directions.DOWN,
            NPArray8Directions.LEFT,
            NPArray8Directions.RIGHT,
            NPArray8Directions.UPRIGHT,
            NPArray8Directions.DOWNRIGHT,
            NPArray8Directions.UPLEFT,
            NPArray8Directions.DOWNLEFT,
        ]
