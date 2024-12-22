from collections import Counter
import copy

import numpy as np
from aoc_utils import read_input

input_secret_numbers = read_input(as_type=int)


def mix(secret_number: int, value: int) -> int:
    return secret_number ^ value


def prune(secret_number: int) -> int:
    return secret_number % 16777216


def naive_secret_number_evolving(secret_number: int) -> int:
    x = secret_number * 64
    secret_number = mix(secret_number, x)
    secret_number = prune(secret_number)

    x = secret_number // 32
    secret_number = mix(secret_number, x)
    secret_number = prune(secret_number)

    x = secret_number * 2048
    secret_number = mix(secret_number, x)
    secret_number = prune(secret_number)

    return secret_number


def find_best_sequence(secret_numbers: list[int]) -> int:
    secret_numbers = copy.copy(secret_numbers)

    price_by_id_by_sequence = [{} for _ in secret_numbers]

    for num_id, secret_number in enumerate(secret_numbers):
        delta_sequence = []
        for _ in range(2000):
            new_secret_number = naive_secret_number_evolving(secret_number)

            price = int(str(new_secret_number)[-1])

            delta = price - int(str(secret_number)[-1])
            secret_number = new_secret_number

            delta_sequence.append(delta)
            if len(delta_sequence) > 4:
                delta_sequence = delta_sequence[-4:]

            if len(delta_sequence) == 4:
                if tuple(delta_sequence) not in price_by_id_by_sequence[num_id]:
                    price_by_id_by_sequence[num_id][tuple(delta_sequence)] = price

    patterns = set(
        [p for p_to_price in price_by_id_by_sequence for p in p_to_price.keys()]
    )
    best_price = 0
    for pattern in patterns:
        pattern_price_sum = 0
        for price_by_sequence in price_by_id_by_sequence:
            pattern_price_sum += price_by_sequence.get(pattern, 0)
        if pattern_price_sum > best_price:
            best_price = pattern_price_sum
    return best_price


# part 1
secret_numbers = copy.copy(input_secret_numbers)
for num_id, secret_number in enumerate(secret_numbers):
    for _ in range(2000):
        secret_number = naive_secret_number_evolving(secret_number)
    secret_numbers[num_id] = secret_number
print(sum(secret_numbers))

# part 2
res = find_best_sequence(input_secret_numbers)
print(res)
