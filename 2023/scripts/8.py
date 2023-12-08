from datetime import datetime

import numpy as np

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


def get_number_of_steps_from_given_start_to_a_z(start: str, directions: str, nodes: dict) -> int:
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

    node_id_to_node_name = [node_name for node_name in nodes]

    nodes_np_graph = np.zeros((2, len(nodes)), dtype=np.int16)  # 2 <=> L/R
    for node_name, left_right_nodes in nodes.items():
        left_node, right_node = left_right_nodes.values()
        nodes_np_graph[0][
            node_id_to_node_name.index(node_name)
        ] = node_id_to_node_name.index(left_node)
        nodes_np_graph[1][
            node_id_to_node_name.index(node_name)
        ] = node_id_to_node_name.index(right_node)

    # Starting and ending nodes
    starting_node_ids = np.array(
        [
            node_id_to_node_name.index(node_name)
            for node_name in nodes
            if node_name.endswith("A")
        ]
    )
    ending_node_ids = np.array(
        [
            node_id_to_node_name.index(node_name)
            for node_name in nodes
            if node_name.endswith("Z")
        ]
    )

    directions = directions.replace("L", "0")
    directions = directions.replace("R", "1")

    current_nodes = np.array(starting_node_ids)

    n_steps = 0
    while True:
        if all(n in ending_node_ids for n in current_nodes):
            break
        direction_to_take = int(directions[n_steps % len(directions)])

        current_nodes = nodes_np_graph[direction_to_take][current_nodes]
        n_steps += 1

    return n_steps


# print("P1", get_number_of_steps_from_aaa_to_zzz(input_directions, input_nodes))
print("P2", get_number_of_steps_from_all_a_to_all_z(input_directions, input_nodes))
