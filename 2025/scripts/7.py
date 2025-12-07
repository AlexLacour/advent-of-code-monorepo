from collections import defaultdict
import copy
from typing import Optional
import numpy as np
from aoc_utils import read_input
from queue import Queue
from aoc_utils.enums.directions import NPArray4Directions


input_tachyon_diagram = read_input(as_type=list, to_numpy=True)

beam_start = tuple(np.argwhere(input_tachyon_diagram == "S")[0])

# beams_to_move: Queue[tuple[int, int]] = Queue()
# beams_to_move.put(beam_start)

# splits = set()

# while beams_to_move.qsize():
#     beam_position = beams_to_move.get()
#     move = tuple(NPArray4Directions.DOWN + beam_position)

#     if move[0] >= len(input_tachyon_diagram):
#         continue

#     if input_tachyon_diagram[move] == ".":
#         input_tachyon_diagram[move] = "|"
#         beams_to_move.put(move)

#     elif input_tachyon_diagram[move] == "^":
#         move_left = tuple(NPArray4Directions.LEFT + move)
#         move_right = tuple(NPArray4Directions.RIGHT + move)

#         splits.add(move)

#         input_tachyon_diagram[move_left] = "|"
#         input_tachyon_diagram[move_right] = "|"

#         beams_to_move.put(move_left)
#         beams_to_move.put(move_right)

# only keep track of vertical axis, they only go down one by one anyway
beams = {beam_start[1]: 1}

splits = 0

for row in input_tachyon_diagram[1:]:
    for beam, paths in copy.deepcopy(beams).items():
        if row[beam] == "^":
            splits += 1
            beams[beam - 1] = beams.get(beam - 1, 0) + paths
            beams[beam + 1] = beams.get(beam + 1, 0) + paths
            beams.pop(beam)

print(splits, sum(beams.values()))
