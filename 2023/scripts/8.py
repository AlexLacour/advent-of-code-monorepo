import math

from aoc_utils import read_input

input_directions, _, *raw_input_nodes = read_input()


def parse_raw_nodes(node_str_list: list[str]) -> dict:
    node_dict = {}
    for node_str in node_str_list:
        node_name, left_right = node_str.split(" = ")

        left, right = left_right.strip("()").split(", ")

        node_dict[node_name] = {"L": left, "R": right}
    return node_dict


input_nodes = parse_raw_nodes(raw_input_nodes)


def get_number_of_steps_from_given_start_to_a_z(
    start: str, directions: str, nodes: dict
) -> int:
    current_node = start
    n_steps = 0
    while not current_node.endswith("Z"):
        direction_to_take = directions[n_steps % len(directions)]
        n_steps += 1
        current_node = nodes[current_node][direction_to_take]

    return n_steps


def get_number_of_steps_from_all_a_to_all_z(
    directions: str, nodes: dict[str, dict]
) -> int:
    # Starting nodes
    starting_nodes = [node_name for node_name in nodes if node_name.endswith("A")]

    n_steps_collection = []
    for starting_node in starting_nodes:
        n_steps_collection.append(
            get_number_of_steps_from_given_start_to_a_z(
                starting_node, directions, nodes
            )
        )

    return math.lcm(*n_steps_collection)


print(
    "P1",
    get_number_of_steps_from_given_start_to_a_z("AAA", input_directions, input_nodes),
)
print("P2", get_number_of_steps_from_all_a_to_all_z(input_directions, input_nodes))
