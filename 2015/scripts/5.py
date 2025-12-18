import re

from aoc_utils import read_input

phrases = read_input()

vowels_regex = r"(?:[^aeiou]*[aeiou][^aeiou]*){3}"
consecutive_chars_regex = r"(?=.*(.)\1)"
forbidden_substring_regex = r".*(?=ab|cd|pq|xy).*"

repeating_pair_regex = r".*(.{2}).*\1+"
repeating_spaced_char_regex = r".*(.).{1}\1"

nice = 0
nicer = 0
for phrase in phrases:
    there_are_three_vowels = bool(re.match(vowels_regex, phrase))
    two_consecutive_chars = bool(re.match(consecutive_chars_regex, phrase))
    forbidden_substring = bool(re.match(forbidden_substring_regex, phrase))

    repeating_pair = bool(re.match(repeating_pair_regex, phrase))
    spaced_repeating_char = bool(re.match(repeating_spaced_char_regex, phrase))

    print(phrase, repeating_pair, spaced_repeating_char)

    nice += (
        there_are_three_vowels
        and two_consecutive_chars
        and not forbidden_substring
    )
    nicer += repeating_pair and spaced_repeating_char

print(nice, nicer)
