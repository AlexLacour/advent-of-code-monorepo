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


class NPArrayDirections:
    UP = np.array((-1, 0))
    DOWN = np.array((1, 0))
    LEFT = np.array((0, -1))
    RIGHT = np.array((0, 1))
