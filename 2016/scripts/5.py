from hashlib import md5

from aoc_utils import read_input

input_door_id = read_input(one_line=True, separator="")


def get_password(door_id: str, positional: bool = False) -> str:
    integer_index = 0

    password = ""
    positional_password_list = ["" for _ in range(8)]
    while True:
        if len(password) >= 8:
            return password
        elif len("".join(positional_password_list)) >= 8:
            return "".join(positional_password_list)

        to_hash = (door_id + str(integer_index)).encode("utf-8")
        door_hash = md5(to_hash).hexdigest()
        integer_index += 1

        if door_hash.startswith("00000"):
            if not positional:
                password += door_hash[5]
            else:
                password_index = door_hash[5]

                if (
                    password_index.isdigit()
                    and int(password_index) < 8
                    and positional_password_list[int(password_index)] == ""
                ):
                    positional_password_list[int(password_index)] = door_hash[6]


print(f"{get_password(input_door_id)=}")
print(f"{get_password(input_door_id, positional=True)=}")
