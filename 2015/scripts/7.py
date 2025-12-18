import copy
from collections import defaultdict, deque

from aoc_utils import read_input


def parse_instruction(instruction_str: str) -> tuple[list[str], str]:
    i, o = instruction_str.split(" -> ")

    return i.split(), o


input_instructions = read_input(as_type=parse_instruction)


def process_instructions(
    instructions: list[tuple[list[str], str]],
    initial_wires: dict[str, int] | None = None,
) -> dict[str, int]:
    wires_values: dict[str, int] = initial_wires or {}

    instructions_to_process = copy.deepcopy(instructions)

    while instructions_to_process:
        instruction, output = instructions_to_process.pop(0)

        if output not in wires_values:
            if len(instruction) == 1 and instruction[0].isnumeric():
                wires_values[output] = int(instruction[0])
            elif len(instruction) == 1 and instruction[0] in wires_values:
                wires_values[output] = wires_values[instruction[0]]
            elif "NOT" in instruction and instruction[1] in wires_values:
                wires_values[output] = ~wires_values[instruction[1]] & 0xFFFF
            elif (
                "OR" in instruction
                and instruction[0] in wires_values
                and instruction[2] in wires_values
            ):
                wires_values[output] = (
                    wires_values[instruction[0]] | wires_values[instruction[2]]
                )
            elif (
                "AND" in instruction
                and instruction[0] in wires_values
                and instruction[2] in wires_values
            ):
                wires_values[output] = (
                    wires_values[instruction[0]] & wires_values[instruction[2]]
                )
            elif (
                "AND" in instruction
                and instruction[0].isnumeric()
                and instruction[2] in wires_values
            ):
                wires_values[output] = (
                    int(instruction[0]) & wires_values[instruction[2]]
                )
            elif "LSHIFT" in instruction and instruction[0] in wires_values:
                wires_values[output] = wires_values[instruction[0]] << int(
                    instruction[2]
                )
            elif "RSHIFT" in instruction and instruction[0] in wires_values:
                wires_values[output] = wires_values[instruction[0]] >> int(
                    instruction[2]
                )
            else:
                instructions_to_process.append((instruction, output))

    return wires_values


wires_values = process_instructions(instructions=input_instructions)
print(wires_values["a"])

initial_values = {"b": wires_values["a"]}
wires_values = process_instructions(
    instructions=input_instructions, initial_wires=initial_values
)
print(wires_values["a"])
