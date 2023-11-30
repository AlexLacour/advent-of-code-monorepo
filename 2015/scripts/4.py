import hashlib

from aoc_utils import read_input

input_word = read_input(one_line=True, separator=None)


def compute_md5(word: str) -> str:
    return hashlib.md5(word.encode("ascii")).hexdigest()


def find_number_giving_specific_hash_start(starting_str_to_find: str = "00000") -> int:
    base_number = 1
    while True:
        if compute_md5(input_word + str(base_number)).startswith(starting_str_to_find):
            break
        base_number += 1
    return base_number


print("P1", find_number_giving_specific_hash_start())
print("P2", find_number_giving_specific_hash_start(starting_str_to_find="000000"))
