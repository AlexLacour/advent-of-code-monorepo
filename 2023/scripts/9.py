from itertools import pairwise

from aoc_utils import read_input

input_histories = read_input(as_type=lambda x: list(map(int, x.split())))


def compute_extrapolation_matrix(history: list[int]):
    extrapolation_matrix = [history]

    difference_list = [y - x for x, y in pairwise(history)]

    extrapolation_matrix.append(difference_list)

    while any(el for el in difference_list):
        difference_list = [y - x for x, y in pairwise(difference_list)]
        extrapolation_matrix.append(difference_list)

    return extrapolation_matrix[::-1]


def predict_next_value(extrapolation_matrix: list[list[int]], direction: str = "right"):
    if direction == "right":
        for pred_line_id, pred_line in enumerate(extrapolation_matrix):
            if pred_line_id == 0:
                pred_line.append(0)
            else:
                left_value = pred_line[-1]
                below_value = extrapolation_matrix[pred_line_id - 1][-1]
                pred_line.append(left_value + below_value)
        next_value = extrapolation_matrix[-1][-1]

    elif direction == "left":
        for pred_line_id, pred_line in enumerate(extrapolation_matrix):
            if pred_line_id == 0:
                pred_line.insert(0, 0)

            else:
                right_value = pred_line[0]
                below_value = extrapolation_matrix[pred_line_id - 1][0]

                pred_line.insert(0, right_value - below_value)
        next_value = extrapolation_matrix[-1][0]
    return next_value


print(
    "P1",
    sum(
        predict_next_value(compute_extrapolation_matrix(history), direction="right")
        for history in input_histories
    ),
)
print(
    "P2",
    sum(
        predict_next_value(compute_extrapolation_matrix(history), direction="left")
        for history in input_histories
    ),
)
