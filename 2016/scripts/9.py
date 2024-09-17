from aoc_utils import read_input

input_compressed_text: str = read_input(one_line=True, separator="")


def get_decompressed_text_len(compressed_text: str, naive: bool = True):
    text_index = 0
    decompressed_text_len = 0
    while text_index < len(compressed_text):
        match compressed_text[text_index]:
            case "(":  # instruction start
                eoi = compressed_text.find(")", text_index)
                seq_length, n_repeats = map(
                    int, compressed_text[text_index + 1 : eoi].split("x")
                )

                text_to_decompress = compressed_text[eoi + 1 : eoi + 1 + seq_length]

                if naive or "(" not in text_to_decompress:
                    decompressed_text_len += len(text_to_decompress) * n_repeats
                else:
                    decompressed_text_len += n_repeats * get_decompressed_text_len(
                        text_to_decompress, naive=False
                    )

                text_index += seq_length + (eoi - text_index) + 1
            case letter:
                decompressed_text_len += 1
                text_index += 1
    return decompressed_text_len


print(f"{get_decompressed_text_len(input_compressed_text)=}")
print(f"{get_decompressed_text_len(input_compressed_text, naive=False)=}")
