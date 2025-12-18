import numpy as np

from aoc_utils import read_input


def parse_distance(node_distance_str: str) -> tuple[str, str, int]:
    cities, distance_str = node_distance_str.split(" = ")
    from_city, to_city = cities.split(" to ")

    return from_city, to_city, int(distance_str)


input_distances = read_input(as_type=parse_distance)

cities_index = set()
for from_city, to_city, _ in input_distances:
    cities_index.add(from_city)
    cities_index.add(to_city)
cities_index = list(cities_index)

dist_matrix = np.zeros((len(cities_index), len(cities_index)))

for from_city, to_city, distance in input_distances:
    dist_matrix[cities_index.index(from_city), cities_index.index(to_city)] = (
        distance
    )
    dist_matrix[cities_index.index(to_city), cities_index.index(from_city)] = (
        distance
    )


print(dist_matrix)
