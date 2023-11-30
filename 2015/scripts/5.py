from aoc_utils import read_input

phrases = read_input()
vowels_regex = "(?:[^aeiou]*[aeiou][^aeiou]*){3}"
consecutive_chars_regex = "(?=.*(.)\1)"
