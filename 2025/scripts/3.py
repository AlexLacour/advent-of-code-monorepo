from aoc_utils import read_input


def parse_bank(bank_line_str: str) -> list[int]:
    return list(map(int, list(bank_line_str)))


def get_total_joltage_output(batteries_bank: list[int], max_batteries: int = 2) -> int:

    max_joltage_arr = []
    arr_len = max_batteries
    last_added_battery_id = -1

    while arr_len:
        battery_range = (
            batteries_bank[last_added_battery_id + 1 : (arr_len - 1) * -1]
            if arr_len > 1
            else batteries_bank[last_added_battery_id + 1 :]
        )
        optimal_battery = max(battery_range)
        last_added_battery_id = (
            battery_range.index(optimal_battery) + last_added_battery_id + 1
        )
        max_joltage_arr.append(optimal_battery)
        arr_len -= 1

    max_joltage = int("".join(map(str, max_joltage_arr)))
    return max_joltage


input_batteries_banks: list[list[int]] = read_input(as_type=parse_bank)
total_output_2 = sum([get_total_joltage_output(bank) for bank in input_batteries_banks])
total_output_12 = sum(
    [get_total_joltage_output(bank, 12) for bank in input_batteries_banks]
)
print(total_output_2, total_output_12)
