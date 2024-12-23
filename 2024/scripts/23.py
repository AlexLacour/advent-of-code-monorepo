from collections import defaultdict
from aoc_utils import read_input
from itertools import combinations
import numpy as np

input_network_map = read_input(as_type=lambda c: c.split("-"))


def get_size3_interconnected_sets(network_map: list) -> list[tuple[str, str, str]]:
    computer_names = set([name for connection in network_map for name in connection])

    computer_connections = defaultdict(list)
    for name in computer_names:
        for cmp1, cmp2 in network_map:
            if name == cmp1:
                computer_connections[name].append(cmp2)
            elif name == cmp2:
                computer_connections[name].append(cmp1)

    interconnected_sets: list[tuple[str, str, str]] = []
    for name, connected_to in computer_connections.items():
        for cmp_id, connected_name in enumerate(connected_to):
            for other_cmp in connected_to[cmp_id + 1 :]:
                if other_cmp in computer_connections[connected_name]:
                    connected_set = sorted((name, connected_name, other_cmp))
                    if connected_set not in interconnected_sets:
                        interconnected_sets.append(connected_set)
    return interconnected_sets


def get_longest_interconnected_set(network_map: list[list[str]]) -> list:
    # max clique problem
    computer_names = sorted(
        list(set([name for connection in network_map for name in connection]))
    )
    computer_connections = defaultdict(set)
    for cmp1, cmp2 in network_map:
        computer_connections[cmp1].add(cmp2)
        computer_connections[cmp2].add(cmp1)

    computer_connections = {
        key: sorted(conns) for key, conns in computer_connections.items()
    }

    # R, P, X and 3 disjointed sets of vertices in a graph with no directions. Finds the maximal clique that includes
    # - all of R
    # - part or P
    # - none of X
    def bron_kerbosch(R: set, P: set, X: set, graph: dict[str, set]):
        if not P and not X:
            yield R
        while P:
            v = P.pop()
            yield from bron_kerbosch(
                R.union({v}), P.intersection(graph[v]), X.intersection(graph[v]), graph
            )
            X.add(v)

    all_cliques = list(
        bron_kerbosch(
            set(), set(computer_connections.keys()), set(), computer_connections
        )
    )
    res = sorted(max(all_cliques, key=len))
    return res


# Part 1
sets_starting_with_t = [
    connected_set
    for connected_set in get_size3_interconnected_sets(input_network_map)
    if any(cmp for cmp in connected_set if cmp.startswith("t"))
]
print(f"{len(sets_starting_with_t)=}")

# Part 2
password = ",".join(get_longest_interconnected_set(input_network_map))
print(f"{password=}")
