import copy
from queue import Queue
from aoc_utils import read_input
import re


def parse_machine(
    machine_init_str: str,
) -> tuple[int, list[int], list[tuple[int, ...]], list[int]]:
    split_machine = machine_init_str.split()

    lights_str = split_machine[0][1:-1]
    n_lights = len(lights_str)
    lights_targets = [i for i, symbol in enumerate(lights_str) if symbol == "#"]

    buttons_wirings_strs = split_machine[1:-1]
    buttons_wirings = [eval(wiring_str) for wiring_str in buttons_wirings_strs]

    joltage_reqs = map(int, split_machine[-1][1:-1].split(","))

    return n_lights, lights_targets, buttons_wirings, list(joltage_reqs)


input_machines = read_input(as_type=parse_machine)

res = 0
for machine in input_machines:
    n_lights, lights_targets, buttons_wirings, _ = machine

    initial_lights_state = [False] * n_lights

    queue = Queue()
    queue.put(
        (copy.copy(initial_lights_state), 0, None)
    )  # lights state, number of pushes, last button pushed

    memory_and_min = {}

    while queue.qsize():
        state, npush, lastpushed = queue.get()

        if [i for i, light in enumerate(state) if light] == lights_targets:
            res += npush
            break
        else:
            available_pushes = [
                (i, wiring)
                for i, wiring in enumerate(buttons_wirings)
                if i != lastpushed
            ]

            for pushed, action in available_pushes:
                if isinstance(action, int):
                    action = (action,)
                new_state = [
                    not light if i in action else light for i, light in enumerate(state)
                ]

                memory_key = tuple(new_state)
                if (
                    memory_key not in memory_and_min
                    or memory_and_min[memory_key] > npush + 1
                ):
                    memory_and_min[memory_key] = npush + 1
                    queue.put((new_state, npush + 1, pushed))

print(res)


### P2
res = 0
for machine in input_machines:
    _, _, buttons_wirings, joltage_reqs = machine

    initial_jstate = [0 for _ in joltage_reqs]

    queue = Queue()

    queue.put(
        (copy.copy(initial_jstate), 0, None)
    )  # lights state, number of pushes, last button pushed

    memory_and_min = {}

    while queue.qsize():
        state, npush, lastpushed = queue.get()

        if state == joltage_reqs:
            res += npush
            break
        else:
            available_pushes = [
                (i, wiring)
                for i, wiring in enumerate(buttons_wirings)
                if i != lastpushed
            ]

            for pushed, action in available_pushes:
                if isinstance(action, int):
                    action = (action,)
                new_state = [
                    jolt + 1 if i in action else jolt for i, jolt in enumerate(state)
                ]

                memory_key = tuple(new_state)
                if (
                    memory_key not in memory_and_min
                    or memory_and_min[memory_key] > npush + 1
                    and all(j < req for j, req in zip(new_state, joltage_reqs))
                ):
                    memory_and_min[memory_key] = npush + 1
                    queue.put((new_state, npush + 1, pushed))

print(res)
