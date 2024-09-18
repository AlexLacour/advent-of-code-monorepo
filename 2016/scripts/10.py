import copy
from typing import Optional

from aoc_utils import read_input

input_bots_instructions = read_input()
input_structures_init_instructions: list[str] = []
start_instructions: list[str] = []
for instruction in input_bots_instructions:
    if "goes to" in instruction:
        start_instructions.append(instruction)
    else:
        input_structures_init_instructions.append(instruction)


class Bot:
    def __init__(self, bot_id: int, initial_values: Optional[list[int]] = None):
        self.bot_id = bot_id
        self.values = initial_values or []
        self.low_destination = None
        self.high_destination = None

        self.look_for_values = None

    def add_value(self, value: int):
        self.values.append(value)
        if len(self.values) >= 2:
            min_value = min(self.values)
            max_value = max(self.values)

            if (
                self.look_for_values
                and min_value in self.look_for_values
                and max_value in self.look_for_values
            ):
                print(f"{self.look_for_values} -> bot {self.bot_id}")

            self.low_destination.add_value(min_value)
            self.high_destination.add_value(max_value)

            self.values.remove(min_value)
            self.values.remove(max_value)


class Output:
    def __init__(self, output_id: int) -> None:
        self.output_id = output_id
        self.values = []

    def add_value(self, value: int):
        self.values.append(value)

    def __repr__(self) -> str:
        return f"Output({self.output_id}) -> {self.values}"


class Memory:
    def __init__(self, structures_init_instructions: list[str]) -> None:
        self.bots: dict[int, Bot] = {}
        self.outputs: dict[int, Output] = {}
        self.__initialize_structures(structures_init_instructions)

    def __initialize_structures(self, structures_init_instructions: list[str]):
        for instruction in structures_init_instructions:
            _, bot_id, _, _, _, low_type, low_id, _, _, _, high_type, high_id = (
                instruction.split()
            )
            bot_id = int(bot_id)
            low_id = int(low_id)
            high_id = int(high_id)

            if bot_id not in self.bots:
                self.bots[bot_id] = Bot(bot_id)

            if low_type == "bot" and low_id not in self.bots:
                self.bots[low_id] = Bot(low_id)
            elif low_type == "output" and low_id not in self.outputs:
                self.outputs[low_id] = Output(low_id)

            if high_type == "bot" and high_id not in self.bots:
                self.bots[high_id] = Bot(high_id)
            elif high_type == "output" and high_id not in self.outputs:
                self.outputs[high_id] = Output(high_id)

            self.bots[bot_id].low_destination = (
                self.bots[low_id] if low_type == "bot" else self.outputs[low_id]
            )
            self.bots[bot_id].high_destination = (
                self.bots[high_id] if high_type == "bot" else self.outputs[high_id]
            )

    def add_value_to_object(self, object_id: int, value: int, object_type: str = "bot"):
        if object_type != "bot":
            self.outputs[object_id].add_value(value)
        else:
            self.bots[object_id].add_value(value)

    def look_for_values(self, values: list[int]):
        for bot in self.bots.values():
            bot.look_for_values = copy.deepcopy(values)

    def get_outputs_product(self, output_ids: list[int]) -> int:
        product = 1
        for output_id in output_ids:
            for val in self.outputs[output_id].values:
                product *= val
        return product


memory = Memory(input_structures_init_instructions)

memory.look_for_values([61, 17])

for instruction in start_instructions:
    _, value, _, _, object_type, object_id = instruction.split()
    memory.add_value_to_object(
        object_id=int(object_id), value=int(value), object_type=object_type
    )

print(f"{memory.get_outputs_product([0, 1, 2])=}")
