import copy
import math
from aoc_utils import read_input

# input parsing
registers_str, program_str = read_input(raw_input=True).split("\n\n")

input_register_a, input_register_b, input_register_c = map(
    lambda s: int(s.split(": ")[-1]), registers_str.split("\n")
)
input_registers = {"a": input_register_a, "b": input_register_b, "c": input_register_c}

input_program = list(map(int, program_str.split(": ")[-1].split(",")))


# script
def combo(registers: dict, operand: int) -> int:
    if operand in [0, 1, 2, 3]:
        return operand
    elif operand == 4:
        return registers["a"]
    elif operand == 5:
        return registers["b"]
    elif operand == 6:
        return registers["c"]
    else:
        raise ValueError(operand)


def run_program(registers: dict, program: list[int]) -> list[int]:
    registers = copy.deepcopy(registers)
    program = copy.deepcopy(program)

    program_pointer = 0

    program_output = []

    while program_pointer < len(program):
        # get code and operand
        opcode, operand = program[program_pointer], program[program_pointer + 1]

        program_pointer_increase = 2
        if opcode == 0:
            # adv division : A / 2**combo(operand) -> truncated int -> A
            res = registers["a"] // (2 ** combo(registers, operand))
            registers["a"] = res

        elif opcode == 1:
            # bxl bitwise xor : B / literal(operand) -> B
            res = registers["b"] ^ operand
            registers["b"] = res

        elif opcode == 2:
            # bst combo(operand) % 8 -> b
            res = combo(registers, operand) % 8
            registers["b"] = res

        elif opcode == 3:
            # jnz if A != 0, program_pointer = operand (and not + 2 after)
            if registers["a"]:
                program_pointer = operand
                program_pointer_increase = 0

        elif opcode == 4:
            # bxc bitwise xor (B, C) -> B
            res = registers["b"] ^ registers["c"]
            registers["b"] = res

        elif opcode == 5:
            # out combo(operand) % 8 -> output array
            res = combo(registers, operand) % 8
            program_output.append(res)

        elif opcode == 6:
            # bdv division : A / 2**combo(operand) -> truncated int -> B
            res = registers["a"] // (2 ** combo(registers, operand))
            registers["b"] = res

        elif opcode == 7:
            # cdv division : A / 2**combo(operand) -> truncated int -> C
            res = registers["a"] // (2 ** combo(registers, operand))
            registers["c"] = res

        else:
            raise ValueError(opcode)

        program_pointer += program_pointer_increase

    return program_output


# part 1
out = run_program(input_registers, input_program)
out_str = ",".join(map(str, out))
print(f"{out_str=}")

# part 2
# find initial register a's value so that out == supposed_output
# reverse algo:

supposed_output = copy.deepcopy(input_program)


candidates = [0]
for i in range(len(supposed_output)):
    to_get = supposed_output[-(i + 1) :]

    new_candidates = []
    for a_range_start in candidates:
        for a in range(a_range_start, a_range_start + 8):
            registers = {"a": a, "b": 0, "c": 0}
            if (res := run_program(registers, input_program)) == to_get:
                new_candidates.append(a * 8)
    candidates = new_candidates


res = min(candidates) // 8
print(f"{res=}")
