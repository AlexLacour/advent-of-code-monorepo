from math import prod

from aoc_utils import read_input

dimensions_list = read_input(as_type=lambda x: list(map(int, x.split("x"))))


def get_wrapping_paper(l: int, w: int, h: int) -> int:
    sides = [l * w, w * h, h * l]

    required_paper = sum([2 * side for side in sides]) + min(sides)

    return required_paper


def get_total_wrapping_paper(instructions: list) -> int:
    return sum([get_wrapping_paper(*instruction) for instruction in instructions])


def get_ribbon(l: int, w: int, h: int) -> int:
    sorted_dims = sorted([l, w, h])

    return 2 * sum(sorted_dims[:2]) + prod(sorted_dims)


def get_total_ribbon(instructions: list) -> int:
    return sum([get_ribbon(*instruction) for instruction in instructions])


print("P1", get_total_wrapping_paper(dimensions_list))
print("P2", get_total_ribbon(dimensions_list))
