from collections import Counter

from aoc_utils import read_input

input_repeated_message = read_input()


def get_message(repeated_message: list[str], most_common: bool = True) -> str:
    index = 0 if most_common else -1
    message = ""
    for str_column in zip(*repeated_message):
        message += Counter(str_column).most_common()[index][0]
    return message


print(f"{get_message(input_repeated_message)=}")
print(f"{get_message(input_repeated_message, most_common=False)=}")
