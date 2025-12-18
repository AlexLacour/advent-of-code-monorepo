from typing import Any
from aoc_utils import read_input

def parse_outputs(device_output: str) -> tuple[str, set[str]]:
    device_name, outputs = device_output.split(": ")

    return device_name, set(outputs.split())


def dfs_graph_exploration(graph: dict[str, set[str]], node_start: str, node_end: str,
                          necessary_nodes: set[str]) -> dict[str, Any]:
    res = {
        "n-out": 0,
        "n-valid-out": 0
    }
    def graph_step(node: str, history: list[str]):
        for next_node in graph[node]:
            if next_node == node_end:
                res["n-out"] += 1
                if necessary_nodes.issubset(set(history)):
                    res["n-valid-out"] += 1
            else:
                graph_step(next_node, [*history, next_node])
    
    graph_step(node_start, [node_start])

    return res


input_device_outputs = read_input(as_type=parse_outputs)

device_to_outputs = {
    device: outputs for device, outputs in input_device_outputs
}

res = dfs_graph_exploration(device_to_outputs, "you", "out", necessary_nodes={"dac", "fft"})
print(res)
