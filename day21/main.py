"""
Advent of Code 2024, Day 21
Keypad Conundrum
https://adventofcode.com/2024/day/21
"""

import re
from os import path

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


NUMBER_REGEX = re.compile(r"\d+")


def read_codes(file_path: str) -> list[str]:
    """Read door codes from a file."""

    with open(file_path, encoding="utf-8") as file:
        return file.read().splitlines()


def get_length_shortest_input_sequence(code: str) -> int:
    """Calculate the length of the shortest input sequence needed to input the code."""

    return 1


def read_numeric_part(code: str) -> int:
    """Read the numeric part of a door code."""

    re_match = re.search(NUMBER_REGEX, code)
    if re_match:
        return int(re_match.group(0))

    raise ValueError("No numeric part found in code.")


def get_code_complexity(code: str) -> int:
    """Calculate the complexity of a door code."""

    shortest_input_sequence_length = get_length_shortest_input_sequence(code)
    numeric_part = read_numeric_part(code)

    return shortest_input_sequence_length * numeric_part


def main() -> None:
    """Read door codes from a file and process them."""

    input_file = TEST_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    codes = read_codes(file_path)
    print(codes)

    code_complexities = [get_code_complexity(code) for code in codes]
    print(code_complexities)
    print(sum(code_complexities))


if __name__ == "__main__":
    main()
