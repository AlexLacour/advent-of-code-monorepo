from collections import Counter
import copy
from aoc_utils import read_input


def manual_blink(stones: list[int]) -> list[int]:
    new_stones = []
    for stone_number in stones:
        if stone_number == 0:
            new_stones.append(1)
        elif (num_len := len(str(stone_number))) % 2 == 0:
            left_number = int(str(stone_number)[: num_len // 2])
            right_number = int(str(stone_number)[num_len // 2 :])

            new_stones.extend([left_number, right_number])
        else:
            new_stones.append(stone_number * 2024)

    return new_stones


def hash_blink(stones: dict[int, int]) -> dict[int, int]:
    new_stones = {}

    for stone_number, number_count in stones.items():
        blinked_stone_result = manual_blink([stone_number])
        for resulting_stone in blinked_stone_result:
            new_stones[resulting_stone] = number_count + new_stones.get(
                resulting_stone, 0
            )

    return new_stones


def blink_many(times: int, stones: list[int]) -> int:
    stones_counter = dict(Counter(stones))
    for _ in range(times):
        stones_counter = hash_blink(stones_counter)
    return sum(stones_counter.values())


input_stones: list[int] = read_input(
    as_type=lambda line: list(map(int, line.split())), one_line=True, separator=None
)

print(f"{blink_many(25, input_stones)=}")
print(f"{blink_many(75, input_stones)=}")
