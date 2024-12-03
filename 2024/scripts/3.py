from aoc_utils import read_input
import re
import math

input_memory = read_input(raw_input=True)


instructions = re.findall(r"mul\(\d{1,3},\d{1,3}\)", input_memory)
muls = list(map(lambda i: math.prod(map(int, re.findall(r"\d+", i))), instructions))
print(f"{sum(muls)=}")

full_instructions = re.findall(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)", input_memory)

mul_enabled = True
muls = []
for instruction in full_instructions:
    if instruction == "do()":
        mul_enabled = True
    elif instruction == "don't()":
        mul_enabled = False
    elif mul_enabled:
        muls.append(math.prod(map(int, re.findall(r"\d+", instruction))))

print(f"{sum(muls)=}")
