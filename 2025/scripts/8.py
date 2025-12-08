from collections import defaultdict
import math
from aoc_utils import read_input
import numpy as np
from sklearn.metrics import pairwise_distances
import networkx as nx


def parse_box(box_str: str) -> tuple[int, ...]:
    return tuple(map(int, box_str.split(",")))


input_junction_boxes = read_input(as_type=parse_box)

junction_boxes_np = np.asarray(input_junction_boxes)

distances = pairwise_distances(junction_boxes_np, junction_boxes_np)
distances[distances == 0] = np.inf

associations = np.unravel_index(np.argsort(distances, axis=None), distances.shape)[0]

pairs = [
    (
        input_junction_boxes[int(associations[2 * i])],
        input_junction_boxes[int(associations[2 * i + 1])],
    )
    for i in range(len(associations) // 2)
]

g = nx.Graph()
g.add_edges_from(pairs[:1000])
res = sorted(nx.connected_components(g), key=len, reverse=True)[:3]

print(math.prod([len(c) for c in res]))

for pair in pairs[1000:]:
    g.add_edge(*pair)
    if nx.is_connected(g) and len(g) == len(input_junction_boxes):
        break

print(pair[0][0] * pair[1][0])
