import copy
from collections import defaultdict
from itertools import combinations
from queue import Queue
from time import perf_counter
from typing import Any, Optional

from aoc_utils import read_input

input_floors_base_state = read_input()

building_state: list[list[tuple[str, str]]] = []
for floor_id, floor_line in enumerate(input_floors_base_state):
    floor_content: list[tuple[str, str]] = []
    split_sentence = floor_line.split()

    for word_id, word in enumerate(split_sentence):
        word = word.replace(",", "").replace(".", "")
        if word in ["microchip", "generator"]:
            floor_content.append((split_sentence[word_id - 1].split("-")[0], word))
    building_state.append(floor_content)


class State:
    def __init__(
        self,
        current_floor: int,
        floors_layout: list[list[tuple[str, str]]],
        cost: int = 0,
    ) -> None:
        self.floors_layout = floors_layout
        self.current_floor = current_floor
        self.cost = cost

    def __str__(self) -> str:
        return f"{self.current_floor};{self.floors_layout}"

    def is_equivalent_to(self, other_state: "State") -> bool:
        pairs_dict = defaultdict(list)
        for floor_id, floor in enumerate(self.floors_layout):
            for element_obj_type in floor:
                element, obj_type = element_obj_type
                pairs_dict[element].append((floor_id, obj_type))
        pairs = [
            tuple(sorted(pair, key=lambda p: p[1])) for pair in pairs_dict.values()
        ]

        other_pairs_dict = defaultdict(list)
        for floor_id, floor in enumerate(other_state.floors_layout):
            for element_obj_type in floor:
                element, obj_type = element_obj_type
                other_pairs_dict[element].append((floor_id, obj_type))
        other_pairs = [
            tuple(sorted(pair, key=lambda p: p[1]))
            for pair in other_pairs_dict.values()
        ]

        if pairs == other_pairs and self.current_floor == other_state.current_floor:
            return True
        return False

    def get_possible_states(self, seen_states: set["State"]) -> list["State"]:
        possible_states = []

        # move 1 or 2 items
        items_to_move = [
            *combinations(self.floors_layout[self.current_floor], 1),
            *combinations(self.floors_layout[self.current_floor], 2),
        ]
        # up or down
        directions = []
        if self.current_floor < len(self.floors_layout) - 1:
            directions.append(1)
        if self.current_floor > 0 and any(
            [item for row in self.floors_layout[: self.current_floor] for item in row]
        ):
            directions.append(-1)

        for direction in directions:
            new_floor = self.current_floor + direction
            for moved in items_to_move:
                new_layout = copy.deepcopy(self.floors_layout)
                for item in moved:
                    new_layout[self.current_floor].remove(item)
                    new_layout[new_floor].append(item)

                new_state = State(
                    current_floor=new_floor,
                    floors_layout=new_layout,
                    cost=self.cost + 1,
                )

                if new_state.is_valid() and not any(
                    [
                        new_state.is_equivalent_to(prec_state)
                        for prec_state in possible_states
                        if prec_state
                    ]
                ):
                    possible_states.append(new_state)
                else:
                    possible_states.append(None)

        # total_moves = [
        #     (direction, moved) for direction in directions for moved in items_to_move
        # ]
        # for state_id, (direction, moved_items) in enumerate(total_moves):
        #     if direction > 0 and len(moved_items) == 2:
        #         for state_id, (other_direction, other_moved_items) in enumerate(
        #             total_moves
        #         ):
        #             if (
        #                 possible_states[state_id]
        #                 and other_direction == direction
        #                 and len(other_moved_items) == 1
        #             ):
        #                 possible_states[state_id] = None

        #     elif direction < 0 and len(moved_items) == 1:
        #         for state_id, (other_direction, other_moved_items) in enumerate(
        #             total_moves
        #         ):
        #             if (
        #                 possible_states[state_id]
        #                 and other_direction == direction
        #                 and len(other_moved_items) == 2
        #             ):
        #                 possible_states[state_id] = None

        possible_states = [
            state
            for state in possible_states
            if state is not None and state not in seen_states
        ]

        # pruning
        pruned_new_states = []
        ## Eliminate equivalent steps
        for _, state in enumerate(possible_states):
            for seen_state in seen_states:
                if state.is_equivalent_to(seen_state):
                    break
            else:
                pruned_new_states.append(state)

        return pruned_new_states

    def is_valid(self) -> bool:
        for floor in self.floors_layout:
            microchips = [item[0] for item in floor if item[1] == "microchip"]
            generators = [item[0] for item in floor if item[1] == "generator"]

            for microchip_name in microchips:
                if (
                    generators and microchip_name not in generators
                ):  # the microchip is not safe
                    return False
        return True

    def is_endpoint(self) -> bool:
        for floor in self.floors_layout[:-1]:
            if len(floor):
                return False
        return True


# GRAPH CONSTRUCTION & BFS
__start = perf_counter()

initial_state = State(current_floor=0, floors_layout=copy.deepcopy(building_state))

bfs_queue: list[State] = []
seen_states: set[State] = set([initial_state])

bfs_queue.append(initial_state)
while bfs_queue:
    # bfs_queue = sorted(bfs_queue, key=lambda s: s.cost)
    state = bfs_queue.pop(0)

    if state.is_endpoint():
        break

    new_states = state.get_possible_states(seen_states=seen_states)

    for new_state in new_states:
        if new_state not in seen_states:
            bfs_queue.append(new_state)
            seen_states.add(new_state)
else:
    print(
        "===\nFAILURE to reach a satisfying ending step, DON'T take the cost and timing into account !\n==="
    )

print(f"{state.cost=}")
print(f"({perf_counter() - __start})")
