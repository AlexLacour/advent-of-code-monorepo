from collections import Counter

from aoc_utils import read_input

# CONSTANTS
P1_POKER_VALUES = [*[str(int_val) for int_val in range(2, 10)], "T", "J", "Q", "K", "A"]


P2_POKER_VALUES = ["J", *[str(int_val) for int_val in range(2, 10)], "T", "Q", "K", "A"]


POKER_HAND_TYPES = [
    "high_card",
    "one_pair",
    "two_pair",
    "three_of_a_kind",
    "full_house",
    "four_of_a_kind",
    "five_of_a_kind",
]


def parse_hand(hand_str: str) -> tuple:
    hand, bid = hand_str.split()
    return hand, int(bid)


input_poker_hands = read_input(as_type=parse_hand)


def get_ranking(
    poker_hands: list, used_poker_values: list, wild_card: bool = False
) -> list:
    # FIRST SORTING
    hand_types = {hand_type: [] for hand_type in POKER_HAND_TYPES}
    for hand_id, (poker_hand, _) in enumerate(poker_hands):
        counter = Counter(poker_hand)

        if wild_card:
            if len(counter) >= 2 and "J" in counter:
                counter.pop("J")
            most_common, _ = counter.most_common(1)[0]

            wild_card_hand = poker_hand.replace("J", most_common)

            counter = Counter(wild_card_hand)

        if 5 in counter.values():
            hand_types["five_of_a_kind"].append(hand_id)

        elif 4 in counter.values():
            hand_types["four_of_a_kind"].append(hand_id)

        elif 3 in counter.values() and 2 in counter.values():
            hand_types["full_house"].append(hand_id)

        elif 3 in counter.values():
            hand_types["three_of_a_kind"].append(hand_id)

        elif 2 in counter.values() and Counter(counter.values())[2] == 2:
            hand_types["two_pair"].append(hand_id)

        elif 2 in counter.values():
            hand_types["one_pair"].append(hand_id)

        else:
            hand_types["high_card"].append(hand_id)

    # RANKING
    ranking = []
    for _, candidates_ids in hand_types.items():
        if candidates_ids:
            if len(candidates_ids) == 1:
                ranking.append(candidates_ids[0])
                continue

            candidates_hands = {
                candidate: input_poker_hands[candidate][0]
                for candidate in candidates_ids
            }

            candidates_hands_with_int_values = {
                hand_id: [used_poker_values.index(hand_value) for hand_value in hand]
                for hand_id, hand in candidates_hands.items()
            }
            sorted_hands = sorted(
                candidates_hands_with_int_values.items(), key=lambda x: x[1]
            )

            for hand_id, _ in sorted_hands:
                ranking.append(hand_id)

    return ranking


def get_total_winning(poker_hands: list, ranking: list) -> int:
    total_winning = 0
    for ranking_id, hand_id in enumerate(ranking):
        _, bid = poker_hands[hand_id]
        total_winning += (ranking_id + 1) * bid
    return total_winning


print(
    "P1",
    get_total_winning(
        input_poker_hands,
        get_ranking(input_poker_hands, P1_POKER_VALUES, wild_card=False),
    ),
)
print(
    "P2",
    get_total_winning(
        input_poker_hands,
        get_ranking(input_poker_hands, P2_POKER_VALUES, wild_card=True),
    ),
)
