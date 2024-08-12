from aoc_utils import read_input

input_triangles = read_input(as_type=lambda coords: list(map(int, coords.split())))

side_combinations = [(0, 1, 2), (1, 2, 0), (2, 0, 1)]


def get_possible_triangles(triangles_list: list[list[int]]) -> list[list[int]]:
    possible_triangles = []
    for triangle_coords in triangles_list:
        if all(
            [
                (triangle_coords[first_side] + triangle_coords[second_side])
                > triangle_coords[remaining_side]
                for first_side, second_side, remaining_side in side_combinations
            ]
        ):
            possible_triangles.append(possible_triangles)
    return possible_triangles


print(f"{len(get_possible_triangles(input_triangles))=}")

triangle_columns_list = [val for vals in list(zip(*input_triangles)) for val in vals]
triangles_list = list(zip(*(iter(triangle_columns_list),) * 3))
print(f"{len(get_possible_triangles(triangles_list))=}")
