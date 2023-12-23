import shapely

from aoc_utils import read_input


class FallingBlock:
    def __init__(self, first_point: list[int], second_point: list[int]):
        self.first_point = first_point
        self.second_point = second_point

    @property
    def min_z(self):
        return min(self.first_point[2], self.second_point[2])

    @property
    def max_z(self):
        return max(self.first_point[2], self.second_point[2])
    

    def fall(self, by: int = 1):
        self.first_point[-1] = max(1, self.first_point[-1] - by)
        self.second_point[-1] = max(1, self.second_point[-1] - by)

    def __repr__(self):
        return f"{self.first_point, self.second_point}"
    
    def intersects(self, other_block: "FallingBlock") -> bool:
        ab_line = self.first_point[:2], self.second_point[:2]
        cd_line = other_block.first_point[:2], other_block.second_point[:2]

        (ax, ay), (bx, by) = ab_line
        (cx, cy), (dx, dy) = cd_line

        if ax == bx:
            ab_line_list = [(ax, i) for i in range(min(ay, by), max(ay, by) + 1)]
        elif ay == by:
            ab_line_list = [(i, ay) for i in range(min(ax, bx), max(ax, bx) + 1)]

        if cx == dx:
            cd_line_list = [(cx, i) for i in range(min(cy, dy), max(cy, dy) + 1)]
        elif cy == dy:
            cd_line_list = [(i, cy) for i in range(min(cx, dx), max(cx, dx) + 1)]

        return set(ab_line_list).intersection(set(cd_line_list))
        

input_blocks = read_input(
    as_type=lambda line_str: list(
        map(lambda coord_str: list(map(int, coord_str.split(","))), line_str.split("~"))
    )
)

falling_blocks = sorted(
    [FallingBlock(*block) for block in input_blocks],
    key=lambda block: block.min_z
)

for block_id, block in enumerate(falling_blocks):
    blocks_underneath = [underneath_block for underneath_block in falling_blocks[:block_id]
                         if block.intersects(underneath_block)]
    limit_height = blocks_underneath[-1].max_z + 1 if blocks_underneath else 1

    falling_blocks[block_id].fall(by=block.min_z - limit_height)

falling_blocks = sorted(
    falling_blocks,
    key=lambda block: block.min_z
)

supporting = {}
for block_id, block in enumerate(falling_blocks):
    beneath_blocks = [underneath_block for underneath_block in falling_blocks[:block_id]
                      if block.intersects(underneath_block) and underneath_block.max_z == block.min_z - 1]

    print(block_id, beneath_blocks)
