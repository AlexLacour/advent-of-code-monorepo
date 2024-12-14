import copy
import os
import sys
import time
from aoc_utils import read_input
import numpy as np


class Robot:
    def __init__(self, position: tuple[int, int], velocity: tuple[int, int]):
        self.p = np.asarray(position)
        self.v = np.asarray(velocity)

    @property
    def display_position(self):
        return tuple(self.p)[::-1]

    @staticmethod
    def from_str(position_velocity_str: str) -> "Robot":
        position_str, velocity_str = position_velocity_str.split()
        position = eval(f"({position_str.split('=')[-1]})")
        velocity = eval(f"({velocity_str.split('=')[-1]})")

        return Robot(position=position, velocity=velocity)

    def move(self, space_shape: tuple[int, int], move_len: int = 1):
        self.p += self.v * move_len

        for axis, bound in enumerate(space_shape[::-1]):
            if self.p[axis] < 0:
                self.p[axis] = bound - (abs(self.p[axis]) % bound)
            self.p[axis] = self.p[axis] % bound

    def __repr__(self) -> str:
        return f"Robot[p={tuple(self.p)} v={tuple(self.v)}]"


def space_to_quadrants(space: np.ndarray) -> np.ndarray:
    h, w = space.shape
    quadrant_h, quadrant_w = h // 2, w // 2

    first_quadrant = space[:quadrant_h, :quadrant_w]
    second_quadrant = space[:quadrant_h, quadrant_w + 1 :]
    third_quadrant = space[quadrant_h + 1 :, :quadrant_w]
    fourth_quadrant = space[quadrant_h + 1 :, quadrant_w + 1 :]

    return np.stack([first_quadrant, second_quadrant, third_quadrant, fourth_quadrant])


def get_safety_factor(space: np.ndarray):
    quadrants = space_to_quadrants(space)
    quadrants_safety = np.sum(quadrants, axis=(1, 2))
    safety_factor = np.prod(quadrants_safety, dtype=int)

    return safety_factor


input_robots: list[Robot] = read_input(as_type=Robot.from_str)

tiles_tall = 103
tiles_wide = 101
robots_space = np.zeros((tiles_tall, tiles_wide))

for robot in copy.deepcopy(input_robots):
    robot.move(robots_space.shape, move_len=100)
    robots_space[robot.display_position] += 1

safety_factor = get_safety_factor(copy.deepcopy(robots_space))

print(f"{safety_factor=}")

# part 2
initial_move = 6000

for robot in input_robots:
    robot.move(robots_space.shape, move_len=initial_move)

elapsed = initial_move
np.set_printoptions(threshold=sys.maxsize)
try:
    while True:
        elapsed += 1
        robots_space = np.zeros((tiles_tall, tiles_wide))
        for robot in input_robots:
            robot.move(robots_space.shape, move_len=1)
            robots_space[robot.display_position] += 1

        # display
        print(f"\nSpace at {elapsed}s...")
        for row in robots_space:
            row_str = "".join(
                [" " * 2 if value == 0 else chr(9608) * 2 for value in row]
            )
            print(row_str)
        # reset
        input()
        os.system("clear")


except KeyboardInterrupt:
    print(f"Exit after {elapsed}s !")  # 6668 iterations...
