from aoc_utils import read_input
import itertools
import operator


def parse_equation(equation_line: str) -> tuple[int, list[int]]:
    res, terms = equation_line.split(": ")
    terms = terms.split()

    res = int(res)
    terms = list(map(int, terms))

    return res, terms


input_equations = read_input(as_type=parse_equation)


def concatenate_operator(a: int, b: int) -> int:
    return int(str(a) + str(b))


def is_equation_true(
    equation: tuple[int, list[int]], operators: tuple = (operator.mul, operator.add)
) -> bool:
    result, terms = equation

    n_ops = len(terms) - 1

    possible_sequences = [ops for ops in itertools.product(operators, repeat=n_ops)]

    for ops_sequence in possible_sequences:
        number = terms[0]
        for i, op in enumerate(ops_sequence):
            number = op(number, terms[i + 1])

        if number == result:
            return True

    return False


# part 1
calibration_result = sum(
    [equation[0] for equation in input_equations if is_equation_true(equation)]
)
print(f"{calibration_result=}")

# part 2
calibration_result = sum(
    [
        equation[0]
        for equation in input_equations
        if is_equation_true(
            equation, operators=(operator.mul, operator.add, concatenate_operator)
        )
    ]
)
print(f"{calibration_result=}")
