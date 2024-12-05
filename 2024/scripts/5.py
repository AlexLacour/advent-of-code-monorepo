from aoc_utils import read_input


def is_update_in_right_order(
    update_content: list[int], update_rules: list[list[int]]
) -> bool:
    for update_rule in update_rules:
        before, after = update_rule
        if set(update_rule).issubset(update_content) and not (
            update_content.index(before) < update_content.index(after)
        ):
            return False

    return True


def sort_incorrect_update(
    update_content: list[int], update_rules: list[list[int]]
) -> list[int]:
    relevant_rules = [
        rule for rule in update_rules if set(rule).issubset(update_content)
    ]

    while not is_update_in_right_order(update_content, relevant_rules):
        for update_rule in relevant_rules:
            before, after = update_rule
            if not (
                (before_index := update_content.index(before))
                < (after_index := update_content.index(after))
            ):
                update_content[before_index] = after
                update_content[after_index] = before

    return update_content


# start
input_updates = read_input(raw_input=True)
input_update_rules, input_update_contents = input_updates.split("\n\n")

# input parsing
input_update_rules = list(
    map(lambda line: list(map(int, line.split("|"))), input_update_rules.split("\n"))
)
input_update_contents = list(
    map(lambda line: list(map(int, line.split(","))), input_update_contents.split("\n"))
)

are_updates_correct = [
    is_update_in_right_order(update_content, input_update_rules)
    for update_content in input_update_contents
]

correct_updates = [
    update
    for update, correct in zip(input_update_contents, are_updates_correct)
    if correct
]
incorrect_updates = [
    update
    for update, correct in zip(input_update_contents, are_updates_correct)
    if not correct
]

# Part 1
middle_page_numbers = [update[len(update) // 2] for update in correct_updates]
print(f"{sum(middle_page_numbers)=}")

# Part 2
sorted_updates = [
    sort_incorrect_update(update, input_update_rules) for update in incorrect_updates
]
middle_page_numbers = [update[len(update) // 2] for update in sorted_updates]
print(f"{sum(middle_page_numbers)=}")
