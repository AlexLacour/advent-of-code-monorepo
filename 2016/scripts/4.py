from collections import Counter, defaultdict

from aoc_utils import read_input
from aoc_utils.constants import ALPHABET


def _room_str_converter(room_str: str) -> tuple[list[str], int, str]:
    room_name, room_id_checksum = room_str.split("-")[:-1], room_str.split("-")[-1]
    
    room_id, checksum = int(room_id_checksum.split("[")[0]), room_id_checksum.split("[")[1][:-1]
    
    return room_name, room_id, checksum


def name_to_checksum(room_name: str) -> str:
    letters_count = Counter(room_name)
    
    letters_by_value = defaultdict(list)
    
    for letter, value in letters_count.items():
        letters_by_value[value].append(letter)
    
    checksum = []
    
    for value in sorted(letters_by_value, reverse=True):
        checksum.extend(sorted(letters_by_value[value]))

    return "".join(checksum[:5])


def decrypt_room_name(room_words: list[str], room_id: int) -> str:
    room_name_list = []
    for word in room_words:
        room_name_list.append("")
        for letter in word:
            decrypted_letter_index = (ALPHABET.index(letter) + room_id) % len(ALPHABET)
            room_name_list[-1] += ALPHABET[decrypted_letter_index]
    return " ".join(room_name_list)


rooms_input = read_input(as_type=_room_str_converter)

real_rooms_ids = []
room_names = []
for room_name, room_id, room_checksum in rooms_input:
    if name_to_checksum("".join(room_name)) == room_checksum:
        real_rooms_ids.append(room_id)
        room_names.append(decrypt_room_name(room_name, room_id))

print(f"{sum(real_rooms_ids)=}")
print(f"{real_rooms_ids[room_names.index('northpole object storage')]=}")
