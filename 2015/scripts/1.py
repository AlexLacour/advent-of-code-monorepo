from typing import Optional

from aoc_utils import read_input

instructions = read_input(one_line=True, separator=None)


def run_instructions(instructions: str, target: Optional[int] = None) -> int:
    level = 0
    for instruction_id, instruction in enumerate(instructions):
        if instruction == "(":
            level += 1
        elif instruction == ")":
            level -= 1
        if target and level == target:
            return instruction_id + 1
    return level


print("P1", run_instructions(instructions))
print("P2", run_instructions(instructions, target=-1))
