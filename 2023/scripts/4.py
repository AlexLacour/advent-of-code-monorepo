from aoc_utils import read_input


def parse_input(card_str: str) -> dict:
    card_id, card_lists = card_str.split(":")

    card_id_int = int(card_id.split()[-1])

    winning_nums, got_nums = card_lists.split("|")

    winning_nums_list = list(map(int, winning_nums.split()))
    got_nums_list = list(map(int, got_nums.split()))

    return {"id": card_id_int, "winning": winning_nums_list, "got": got_nums_list}


input_scratch_cards = read_input(as_type=parse_input)


def compute_matches(first_list: list, second_list: list) -> list:
    return [val for val in second_list if val in first_list]


def part1(scratch_cards: list):
    total_score = 0
    for scratch_card_info in scratch_cards:
        matches = compute_matches(
            scratch_card_info["winning"], scratch_card_info["got"]
        )
        score = 2 ** (len(matches) - 1) if matches else 0
        total_score += score

    return total_score


def part2(scratch_cards: list):
    n_cards = {card["id"]: 1 for card in scratch_cards}

    n_matches_per_card = {
        card["id"]: len(compute_matches(card["winning"], card["got"]))
        for card in scratch_cards
    }

    for card_id in n_cards:
        for i in range(n_matches_per_card[card_id]):
            n_cards[card_id + i + 1] += n_cards[card_id]

    return sum(n_cards.values())


print("P1", part1(input_scratch_cards))
print("P2", part2(input_scratch_cards))
