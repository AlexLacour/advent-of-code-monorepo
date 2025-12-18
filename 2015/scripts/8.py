from aoc_utils import read_input

input_strings = read_input()
code_lens = [len(s) for s in input_strings]
litt_lens = [len(eval(s)) for s in input_strings]

res = sum(code_lens) - sum(litt_lens)
print(res)


def build_extended_repr(string: str) -> str:
    extended_str = '"'
    for c in string:
        if c in ['"', "\\"]:
            extended_str += "\\"

        extended_str += c
    return extended_str + '"'


extended = [len(build_extended_repr(s)) for s in input_strings]

res = sum(extended) - sum(code_lens)
print(res)
