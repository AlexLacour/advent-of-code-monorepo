import math

from aoc_utils import read_input


def str_record_to_dict(str_record: str) -> dict:
    game_number, game_info = str_record.split(":")
    game_number_int = int(game_number.split()[-1])

    game_sets = game_info.split(";")

    game_results = []
    for game_set in game_sets:
        game_cubes = [
            number_of_cubes.split() for number_of_cubes in game_set.split(",")
        ]
        game_cubes_dict = {color: int(number) for number, color in game_cubes}
        game_set_cubes = {"red": 0, "green": 0, "blue": 0, **game_cubes_dict}
        game_results.append(game_set_cubes)

    return {"id": game_number_int, "results": game_results}


games_records = read_input(as_type=str_record_to_dict)


def is_game_possible(
    game_records: dict, red_target: int, green_target: int, blue_target: int
) -> bool:
    for set_cubes in game_records["results"]:
        if (
            set_cubes["red"] > red_target
            or set_cubes["blue"] > blue_target
            or set_cubes["green"] > green_target
        ):
            return False
    return True


def find_rgb_values(game_records: dict) -> tuple[int, int, int]:
    red_value = max([result["red"] for result in game_records["results"]])
    green_value = max([result["green"] for result in game_records["results"]])
    blue_value = max([result["blue"] for result in game_records["results"]])
    return red_value, green_value, blue_value


print(
    "P1",
    sum([game["id"] for game in games_records if is_game_possible(game, 12, 13, 14)]),
)
print("P2", sum([math.prod(find_rgb_values(game)) for game in games_records]))
