from collections import defaultdict

from aoc_utils import read_input


class Broadcaster:
    def __init__(self, name: str, nexts: list[str]):
        self.name = name
        self.nexts = nexts

    def receive_and_get_signal(self, signal: int, from_module: str = None):
        return signal


class FlipFlop:
    def __init__(self, name: str, nexts: list[str]):
        self.name = name
        self.nexts = nexts
        self.state = False  # off

    def receive_and_get_signal(self, signal: int, from_module: str = None) -> int:
        if signal:  # high
            return None
        else:  # low
            self.state = not self.state
            return int(self.state)


class Conjunction:
    def __init__(self, name: str, nexts: list[str]):
        self.name = name
        self.nexts = nexts
        self.memory = None

    def set_memory(self, inputs: list[str]):
        self.memory = {input_str: 0 for input_str in inputs}

    def receive_and_get_signal(self, signal: int, from_module: str) -> int:
        self.memory[from_module] = signal
        if all(self.memory.values()):
            return 0
        return 1


def get_modules(instructions: list) -> dict:
    modules = {}
    conjunctions_modules = []
    for instruction in instructions:
        raw_module_name, nexts_str = instruction.split(" -> ")
        nexts = nexts_str.replace(" ", "").split(",")

        if raw_module_name == "broadcaster":
            module_name = raw_module_name
            modules[module_name] = Broadcaster(module_name, nexts)
        elif raw_module_name.startswith("%"):
            module_name = raw_module_name[1:]
            modules[module_name] = FlipFlop(module_name, nexts)
        elif raw_module_name.startswith("&"):
            module_name = raw_module_name[1:]
            modules[module_name] = Conjunction(module_name, nexts)
            conjunctions_modules.append(module_name)

    for conj_mod in conjunctions_modules:
        conj_mod_inputs = []
        for in_mod, module in modules.items():
            if conj_mod in module.nexts:
                conj_mod_inputs.append(in_mod)

        modules[conj_mod].set_memory(conj_mod_inputs)
    return modules


def push_button(modules: dict[str, Broadcaster | FlipFlop | Conjunction]) -> tuple:
    module_names = [("broadcaster", (0, "button"))]
    highs = 0
    lows = 0
    while True:
        new_module_names = []
        for module_name, (signal, from_module) in module_names:
            if signal:
                highs += 1
            else:
                lows += 1

            if module_name in modules:
                module = modules[module_name]
                signal_to_send = module.receive_and_get_signal(signal, from_module)
            else:  # output / rx
                signal_to_send = None

            if signal_to_send is not None:
                for next_module in module.nexts:
                    new_module_names.append((next_module, (signal_to_send, module_name)))

        module_names = new_module_names
        if not module_names:
            break
    return lows, highs


def get_state(modules: dict) -> str:
    state_dict = {}
    for name, module in modules.items():
        if hasattr(module, "memory"):
            state_dict[name] = module.memory
        elif hasattr(module, "state"):
            state_dict[name] = module.state
    return str(state_dict)

# script
input_instructions = read_input()

modules = get_modules(input_instructions)

n_button_push = 1000
total_lows = 0
total_highs = 0
for _ in range(n_button_push):
    lows, highs = push_button(modules)
    total_lows += lows
    total_highs += highs
print("P1", total_lows * total_highs)


# modules = get_modules(input_instructions)
# initial_state = get_state(modules)
# n_pushes = 0
# while True:
#     n_pushes += 1
#     ret = push_button(modules)

#     if initial_state == get_state(modules):
#         break

# period = n_pushes
# print(period)
