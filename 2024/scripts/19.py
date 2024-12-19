import copy
from typing import Optional
from aoc_utils import read_input

input_available_patterns, input_desired_designs = read_input(raw_input=True).split(
    "\n\n"
)

input_available_patterns = input_available_patterns.split(", ")
input_desired_designs = input_desired_designs.split("\n")


def find_pattern_arrangement(
    design: str, built_arrangement: Optional[list[str]] = None
) -> list[str]:
    possible_patterns = sorted(
        [pattern for pattern in input_available_patterns if design.startswith(pattern)],
        key=len,
        reverse=True,
    )

    for possible_pattern in possible_patterns:
        if design == possible_pattern:
            res = [*built_arrangement, possible_pattern]
            return res
        else:
            if built_arrangement is None:
                built_arrangement = []
            built_arrangement.append(possible_pattern)
            pattern_arrangement = find_pattern_arrangement(
                design[len(possible_pattern) :], built_arrangement
            )

            if pattern_arrangement is not None:
                return pattern_arrangement

            built_arrangement.clear()
                

def get_num_arrangements(
    design: str
) -> list[list[str]]:
    searched = {}
    def search(design: str):
        if design in searched:
            return searched[design]
        
        num_designs = 0
        
        if not design:
            num_designs = 1
        
        for pattern in input_available_patterns:
            if design.startswith(pattern):
                num_designs += search(design[len(pattern):])
                
        searched[design] = num_designs
        return num_designs
    _ = search(design)
    return searched[design]
    

obtained_designs = {desired_design: find_pattern_arrangement(desired_design) for desired_design in input_desired_designs}
possible_designs = [design for design in obtained_designs.values() if design is not None]

print(f"{len(possible_designs)=}")

num_arrangements = 0
for desired_design in input_desired_designs:
    num_arrangements += get_num_arrangements(desired_design)
print(f"{num_arrangements=}")
