from collections import defaultdict
import math
from aoc_utils import read_input
import numpy as np
from sklearn.metrics import pairwise_distances


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
    for i in range(len(input_junction_boxes) // 2)
]


circuits = defaultdict(list)
point_to_circuit_id = {}
circuit_id = 0

for box1, box2 in pairs[:10]:
    if box1 not in point_to_circuit_id and box2 not in point_to_circuit_id:
        circuits[circuit_id].extend([box1, box2])
        point_to_circuit_id[box1] = circuit_id
        point_to_circuit_id[box2] = circuit_id
        circuit_id += 1

    elif box1 in point_to_circuit_id and box2 not in point_to_circuit_id:
        circuits[point_to_circuit_id.get(box1)].append(box2)
        point_to_circuit_id[box2] = point_to_circuit_id.get(box1)

    elif box1 not in point_to_circuit_id and box2 in point_to_circuit_id:
        circuits[point_to_circuit_id.get(box2)].append(box1)
        point_to_circuit_id[box1] = point_to_circuit_id.get(box2)

    elif (
        box1 in point_to_circuit_id
        and box2 in point_to_circuit_id
        and point_to_circuit_id[box1] != point_to_circuit_id[box2]
    ):
        circuits[point_to_circuit_id.get(box1)].extend(
            circuits[point_to_circuit_id.get(box2)]
        )
        for moved_box in circuits.pop(point_to_circuit_id.get(box2)):
            point_to_circuit_id[moved_box] = point_to_circuit_id[box1]

first_res = sorted([len(c) for c in circuits.values()], reverse=True)[:3]
print(first_res)
