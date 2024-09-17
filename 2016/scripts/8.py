import numpy as np

from aoc_utils import read_input

input_screen_instructions = read_input(as_type=lambda instr: instr.split())


screen = np.zeros((6, 50))

for instruction in input_screen_instructions:
    match instruction[0]:
        case "rect":
            width, height = map(int, instruction[-1].split("x"))
            screen[:height, :width] = 1.0
        case "rotate":
            match instruction[1]:
                case "row":
                    row_id = int(instruction[2].split("=")[-1])
                    shift = int(instruction[-1])

                    screen[row_id] = np.roll(screen[row_id], shift)
                case "column":
                    col_id = int(instruction[2].split("=")[-1])
                    shift = int(instruction[-1])
                    screen[:, col_id] = np.roll(screen[:, col_id], shift)

print(f"{np.sum(screen, dtype=int)=}")

for row in screen:
    row_str = "".join(["\u2588" * 2 if val else " " * 2 for val in row])
    print(row_str)
