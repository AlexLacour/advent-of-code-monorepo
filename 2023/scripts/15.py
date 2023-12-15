from collections import defaultdict

from aoc_utils import read_input

input_character_strings = read_input(one_line=True)


def run_hash(character_string: str) -> int:
    hash_value = 0
    for char in character_string:
        hash_value += ord(char)
        hash_value *= 17
        hash_value = hash_value % 256
    return hash_value


def fill_boxes_with_lenses(
    lens_instruction_strings: list[str],
) -> dict[int, dict[str, int]]:
    boxes = defaultdict(dict)
    for string in lens_instruction_strings:
        sep = "=" if "=" in string else "-"
        label, number = string.split(sep)
        box_id = run_hash(label)

        if sep == "=":
            boxes[box_id][label] = int(number)
        elif label in boxes[box_id]:
            boxes[box_id].pop(label)
    return dict(boxes)


def get_focusing_power(boxes: dict[int, dict[str, int]]) -> int:
    focusing_power = 0
    for box_id, box_lenses in boxes.items():
        for slot_id, lens_power in enumerate(box_lenses.values()):
            focusing_power += (box_id + 1) * (slot_id + 1) * lens_power
    return focusing_power


print("P1", sum(run_hash(string) for string in input_character_strings))
print("P2", get_focusing_power(fill_boxes_with_lenses(input_character_strings)))
