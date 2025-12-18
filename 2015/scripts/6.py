import numpy as np

from aoc_utils import read_input


def parse_light_instruction(
    instruction_str: str,
) -> tuple[tuple[int, int], tuple[int, int], int]:
    split_instruction_str = instruction_str.split()

    if len(split_instruction_str) == 5:
        _, value_str, from_str, _, to_str = instruction_str.split()
        light_value = -1 if value_str == "off" else 1
    else:
        _, from_str, _, to_str = instruction_str.split()
        light_value = 2

    from_point = tuple(eval(from_str))
    to_point = tuple(eval(to_str))

    return from_point, to_point, light_value


input_instructions = read_input(as_type=parse_light_instruction)

lights_map = np.zeros((1000, 1000))

for fp, tp, v in input_instructions:
    lights_map[fp[0] : tp[0] + 1, fp[1] : tp[1] + 1] += v
    lights_map[lights_map < 0] = 0

print(int(np.sum(lights_map)))
