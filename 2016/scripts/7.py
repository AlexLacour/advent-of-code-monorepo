import math

from aoc_utils import read_input

input_ip_addresses = read_input()


def address_to_sequences(ipv7_address: str) -> tuple[list[str], list[str]]:
    split_address = ipv7_address.split("[")
    outside_sequences, hyper_outer_pairs = split_address[:1], split_address[1:]
    hypernet_sequences = []

    for hyper_outer_str in hyper_outer_pairs:
        hyper_seq, outer_seq = hyper_outer_str.split("]")
        outside_sequences.append(outer_seq)
        hypernet_sequences.append(hyper_seq)

    return outside_sequences, hypernet_sequences


def is_abba(abba_candidate_str: str) -> bool:
    for str_id, _ in enumerate(abba_candidate_str):
        substring = abba_candidate_str[str_id : str_id + 4]
        if len(substring) < 4:
            return False

        if substring[:2] == substring[2:][::-1] and substring[0] != substring[1]:
            return True


def supports_tls(ipv7_address: str) -> bool:
    outside_sequences, hypernet_sequences = address_to_sequences(ipv7_address)

    outside_are_abba = sum([is_abba(seq) for seq in outside_sequences])
    hypernets_are_abba = math.prod([not is_abba(seq) for seq in hypernet_sequences])

    return bool(outside_are_abba * hypernets_are_abba)


def get_abas(supernet_sequences: list[str]) -> list[str]:
    abas = []
    for seq in supernet_sequences:
        for str_id, _ in enumerate(seq):
            substring = seq[str_id : str_id + 3]
            if len(substring) < 3:
                break

            if substring[0] == substring[2] and substring[0] != substring[1]:
                abas.append(substring)

    return abas


def supports_ssl(ipv7_address: str) -> bool:
    outside_sequences, hypernet_sequences = address_to_sequences(ipv7_address)

    abas = get_abas(outside_sequences)

    aba_to_bab = lambda aba: "".join([aba[1], aba[0], aba[1]])

    for sequence in hypernet_sequences:
        if any([aba_to_bab(aba) in sequence for aba in abas]):
            return True

    return False


print(f"{sum([supports_tls(address) for address in input_ip_addresses])=}")
print(f"{sum([supports_ssl(address) for address in input_ip_addresses])=}")
