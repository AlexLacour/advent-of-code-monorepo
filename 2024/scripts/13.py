from dataclasses import dataclass
from typing import Optional
from aoc_utils import read_input
from decimal import Decimal


@dataclass
class ClawMachine:
    a_delta_x: int
    a_delta_y: int
    b_delta_x: int
    b_delta_y: int
    prize_x: int
    prize_y: int


def parse_machine(machine_str: str) -> ClawMachine:
    a_line, b_line, prize_line = machine_str.split("\n")

    a_x, a_y = a_line.split(": ")[-1].split(", ")
    b_x, b_y = b_line.split(": ")[-1].split(", ")
    prize_x, prize_y = prize_line.split(": ")[-1].split(", ")

    a_x = int(a_x.split("+")[-1])
    a_y = int(a_y.split("+")[-1])

    b_x = int(b_x.split("+")[-1])
    b_y = int(b_y.split("+")[-1])

    prize_x = int(prize_x.split("=")[-1])
    prize_y = int(prize_y.split("=")[-1])

    return ClawMachine(a_x, a_y, b_x, b_y, prize_x, prize_y)


def solve_machine(
    claw_machine: ClawMachine, prize_offset: Optional[int] = 0
) -> Optional[tuple[int, int]]:
    # the big ass equation
    b_push = (
        (claw_machine.prize_y + prize_offset)
        - claw_machine.a_delta_y
        * (claw_machine.prize_x + prize_offset)
        / claw_machine.a_delta_x
    ) / (
        claw_machine.b_delta_y
        - claw_machine.a_delta_y * claw_machine.b_delta_x / claw_machine.a_delta_x
    )
    a_push = (
        (claw_machine.prize_x + prize_offset) - (claw_machine.b_delta_x * b_push)
    ) / claw_machine.a_delta_x

    # precision handling
    a_push = float(Decimal(a_push).quantize(Decimal(".001")))
    b_push = float(Decimal(b_push).quantize(Decimal(".001")))

    # casting if result is correct
    if a_push.is_integer() and b_push.is_integer():
        return int(a_push), int(b_push)


input_machines = read_input(raw_input=True).split("\n\n")
machines = [parse_machine(machine_str) for machine_str in input_machines]

pushes = [solve_machine(machine) for machine in machines]
tokens = [3 * push[0] + push[1] for push in pushes if push]
print(f"{sum(tokens)=}")

pushes = [solve_machine(machine, prize_offset=10000000000000) for machine in machines]
tokens = [3 * push[0] + push[1] for push in pushes if push]
print(f"{sum(tokens)=}")
