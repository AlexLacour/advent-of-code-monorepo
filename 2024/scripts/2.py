import copy
from aoc_utils import read_input

input_reports = read_input(
    as_type=lambda report_line: list(map(int, report_line.split()))
)


def is_report_safe(report: list[int], with_dampener: bool = False) -> bool:
    variations = [
        next_report_value - report_value
        for report_value, next_report_value in zip(report, report[1:])
    ]

    safe_report = True
    for variation_id, variation in enumerate(variations):
        if variation_id > 0 and variations[variation_id - 1] * variation < 0:
            safe_report = False

        if not variation or abs(variation) > 3:
            safe_report = False

    if with_dampener and not safe_report:
        for val_id, _ in enumerate(report):
            dampened_report = copy.deepcopy(report)
            dampened_report.pop(val_id)

            if is_report_safe(dampened_report):
                safe_report = True
                break

    return safe_report


safe_reports = [is_report_safe(report) for report in input_reports]
dampened_safe_reports = [
    is_report_safe(report, with_dampener=True) for report in input_reports
]

print(f"{sum(safe_reports)=}")
print(f"{sum(dampened_safe_reports)=}")
